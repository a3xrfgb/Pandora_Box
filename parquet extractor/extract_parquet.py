#!/usr/bin/env python3
"""
Extract every .parquet file in this script's folder into ./Data/<file name>/

  - Image / audio / video / other binary columns -> saved as real files
    (includes Hugging Face style {"bytes": ..., "path": ...} columns)
  - Caption-like text columns (text, caption, prompt...) -> .txt next to each media file
  - All other columns -> metadata.csv (one row per record)

Requires:  pip install pyarrow
"""

import csv
import json
import re
import sys
from pathlib import Path

try:
    import pyarrow as pa
    import pyarrow.parquet as pq
except ImportError:
    sys.exit("pyarrow is not installed. Run:  pip install pyarrow")

BATCH_SIZE = 256  # rows read at a time, keeps memory low on big files
CAPTION_COLUMNS = ["caption", "text", "prompt", "description", "captions"]

MAGIC_BYTES = [
    (b"\x89PNG\r\n\x1a\n", ".png"),
    (b"\xff\xd8\xff", ".jpg"),
    (b"GIF87a", ".gif"),
    (b"GIF89a", ".gif"),
    (b"II*\x00", ".tif"),
    (b"MM\x00*", ".tif"),
    (b"\x76\x2f\x31\x01", ".exr"),
    (b"fLaC", ".flac"),
    (b"OggS", ".ogg"),
    (b"ID3", ".mp3"),
    (b"\x1a\x45\xdf\xa3", ".mkv"),
    (b"%PDF", ".pdf"),
    (b"PK\x03\x04", ".zip"),
    (b"BM", ".bmp"),
]


def guess_extension(data: bytes, path_hint: str | None = None) -> str:
    """Work out a file extension from the file's first bytes."""
    if data[:4] == b"RIFF" and len(data) >= 12:
        kind = data[8:12]
        if kind == b"WEBP":
            return ".webp"
        if kind == b"WAVE":
            return ".wav"
        if kind == b"AVI ":
            return ".avi"
    if data[4:8] == b"ftyp":
        return ".mp4"
    for magic, ext in MAGIC_BYTES:
        if data.startswith(magic):
            return ext
    if path_hint and Path(path_hint).suffix:
        return Path(path_hint).suffix.lower()
    return ".bin"


def is_media_type(t: pa.DataType) -> bool:
    """Raw binary, or a struct with a 'bytes' field (Hugging Face Image/Audio)."""
    if pa.types.is_binary(t) or pa.types.is_large_binary(t) or pa.types.is_fixed_size_binary(t):
        return True
    return pa.types.is_struct(t) and t.get_field_index("bytes") != -1


def classify_columns(schema: pa.Schema):
    media, media_lists, values = [], [], []
    for field in schema:
        t = field.type
        if is_media_type(t):
            media.append(field.name)
        elif (pa.types.is_list(t) or pa.types.is_large_list(t)) and is_media_type(t.value_type):
            media_lists.append(field.name)
        else:
            values.append(field.name)
    return media, media_lists, values


def unpack_media(value):
    """Return (bytes, path_hint) from a raw bytes value or a {'bytes','path'} dict."""
    if value is None:
        return None, None
    if isinstance(value, dict):
        return value.get("bytes"), value.get("path")
    return value, None


def safe_name(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*\s]+', "_", name).strip("_") or "col"


def to_csv_value(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, default=str)
    return str(value)


def extract_file(parquet_path: Path, data_dir: Path) -> None:
    out_dir = data_dir / parquet_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    pf = pq.ParquetFile(parquet_path)
    media, media_lists, values = classify_columns(pf.schema_arrow)
    all_media = media + media_lists

    # A caption column becomes .txt files only when there is exactly one media column
    caption_col = None
    if len(all_media) == 1:
        lower_map = {v.lower(): v for v in values}
        caption_col = next((lower_map[c] for c in CAPTION_COLUMNS if c in lower_map), None)

    total_rows = pf.metadata.num_rows
    print(f"\n{parquet_path.name}: {total_rows} rows, {len(pf.schema_arrow)} columns")
    if all_media:
        print(f"  media columns: {', '.join(all_media)}")
    if caption_col:
        print(f"  caption column: {caption_col}")

    csv_path = out_dir / "metadata.csv"
    header = ["index"] + values + [f"{c}_file" for c in all_media]
    files_written = 0
    row_index = 0

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)

        for batch in pf.iter_batches(batch_size=BATCH_SIZE):
            cols = {name: batch.column(name).to_pylist() for name in batch.schema.names}

            for i in range(batch.num_rows):
                stem = f"{row_index:06d}"
                file_refs = []

                for col in all_media:
                    # One media column -> 000001.png, several -> 000001_image.png
                    base = stem if len(all_media) == 1 else f"{stem}_{safe_name(col)}"
                    items = cols[col][i] if col in media_lists else [cols[col][i]]
                    items = items or []
                    names = []
                    for k, item in enumerate(items):
                        data, hint = unpack_media(item)
                        if not data:
                            continue
                        suffix = f"_{k}" if col in media_lists else ""
                        filename = f"{base}{suffix}{guess_extension(data, hint)}"
                        (out_dir / filename).write_bytes(data)
                        names.append(filename)
                        files_written += 1
                    file_refs.append(";".join(names))

                if caption_col and file_refs and file_refs[0]:
                    caption = cols[caption_col][i]
                    if caption is not None:
                        (out_dir / f"{stem}.txt").write_text(to_csv_value(caption), encoding="utf-8")

                writer.writerow([row_index] + [to_csv_value(cols[v][i]) for v in values] + file_refs)
                row_index += 1

            print(f"  {row_index}/{total_rows} rows", end="\r")

    print(f"  done: {files_written} media files + metadata.csv -> {out_dir}")


def main() -> None:
    script_dir = Path(__file__).resolve().parent
    parquet_files = sorted(
        p for p in script_dir.iterdir() if p.is_file() and p.suffix.lower() == ".parquet"
    )

    if not parquet_files:
        print(f"No .parquet files found in {script_dir}")
        return

    data_dir = script_dir / "Data"
    data_dir.mkdir(exist_ok=True)
    print(f"Found {len(parquet_files)} parquet file(s). Output folder: {data_dir}")

    failed = []
    for path in parquet_files:
        try:
            extract_file(path, data_dir)
        except Exception as e:  # keep going if one file is broken
            print(f"\n  ERROR in {path.name}: {e}")
            failed.append(path.name)

    print(f"\nFinished. {len(parquet_files) - len(failed)} OK, {len(failed)} failed.")
    if failed:
        print("Failed: " + ", ".join(failed))


if __name__ == "__main__":
    main()
