@echo off
setlocal
title Parquet Extractor
cd /d "%~dp0"

rem ---- Find Python: try the py launcher first, then python ----
set "PY="
py -3 --version >nul 2>&1
if not errorlevel 1 set "PY=py -3"
if not defined PY (
    python --version >nul 2>&1
    if not errorlevel 1 set "PY=python"
)
if not defined PY (
    echo Python was not found.
    echo Install it from https://www.python.org/downloads/
    echo and tick "Add python.exe to PATH" during setup.
    goto :end
)

rem ---- The script needs Python 3.10 or newer ----
%PY% -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if errorlevel 1 (
    echo Your Python version is too old. Version 3.10 or newer is required.
    %PY% --version
    goto :end
)

rem ---- Make sure the Python script is next to this .bat ----
if not exist "extract_parquet.py" (
    echo extract_parquet.py was not found in:
    echo %~dp0
    echo Put the .bat and the .py file in the same folder.
    goto :end
)

rem ---- Install pyarrow if it is missing ----
%PY% -c "import pyarrow" >nul 2>&1
if errorlevel 1 (
    echo pyarrow is not installed. Installing it now...
    %PY% -m pip install pyarrow
    if errorlevel 1 (
        echo.
        echo Could not install pyarrow. Try running: pip install pyarrow
        goto :end
    )
    echo.
)

rem ---- Run the extractor ----
%PY% "extract_parquet.py"

:end
echo.
pause
endlocal
