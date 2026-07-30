#!/usr/bin/env python3
"""
DC Universe Character Folder Generator
=======================================
Creates one main folder per DC hero/villain (spanning the Nolan Dark
Knight trilogy, the Snyderverse/DCEU, The Batman, and the new DCU under
James Gunn starting with Superman (2025)) and, inside each, subfolders
for that character's OWN signature action scenes only.

No action subfolder is assigned to a character unless it genuinely
matches their powers, weapon, or signature move. Superman gets "Heat
Vision Blasting," Batman does not. Batman gets "Batarang Throwing,"
Wonder Woman does not. Etc.

USAGE
-----
    python dc_folder_generator.py                # creates ./DC_Characters
    python dc_folder_generator.py "D:/MyFolder"  # creates in a custom path

You can freely edit the CHARACTERS dictionary below to add, remove, or
rename characters and their action scenes - the script picks up any
changes automatically.
"""

import os
import sys

# ---------------------------------------------------------------------------
# CHARACTER -> ACTION SCENES
# Each list contains ONLY action scenes that belong to that character's
# specific powers, weapons, or signature moves.
# ---------------------------------------------------------------------------

CHARACTERS = {
    # ---------------------------- HEROES ----------------------------
    "Superman":            ["Heat Vision Blasting", "Flying", "Punching", "Freeze Breathing", "Landing"],
    "Batman":               ["Batarang Throwing", "Grapple Swinging", "Punching", "Gadget Deploying", "Gliding"],
    "Wonder Woman":         ["Lasso Throwing", "Sword Slashing", "Shield Blocking", "Bullet Deflecting", "Flying"],
    "The Flash":             ["Super Speed Running", "Lightning Generating", "Time Traveling", "Phasing"],
    "Aquaman":               ["Trident Throwing", "Water Summoning", "Swimming", "Punching"],
    "Cyborg":                ["Cannon Blasting", "Tech Hacking", "Armor Reshaping"],
    "Green Lantern (Hal Jordan)": ["Ring Constructing", "Flying", "Energy Blasting"],
    "Green Lantern (Guy Gardner)": ["Ring Constructing", "Flying", "Energy Blasting"],
    "Shazam":                ["Lightning Summoning", "Flying", "Punching", "Transforming"],
    "Black Adam":            ["Lightning Blasting", "Flying", "Punching", "Teleporting"],
    "Harley Quinn":          ["Mallet Swinging", "Acrobatic Flipping", "Gun Shooting"],
    "Peacemaker":            ["Gun Shooting", "Helmet Deploying", "Punching"],
    "Blue Beetle":           ["Scarab Armor Forming", "Blade Summoning", "Flying"],
    "Nightwing":             ["Escrima Stick Fighting", "Acrobatic Flipping", "Grapple Swinging"],
    "Batgirl":               ["Gadget Throwing", "Punching", "Grapple Swinging"],
    "Robin":                 ["Staff Fighting", "Acrobatic Flipping"],
    "Green Arrow":           ["Arrow Shooting", "Trick Shot Firing"],
    "Zatanna":               ["Backwards Spell Casting", "Illusion Casting"],
    "Martian Manhunter":     ["Shape-Shifting", "Phasing", "Flying", "Telekinesis"],
    "Supergirl":             ["Heat Vision Blasting", "Flying", "Punching"],
    "Mera":                  ["Water Manipulating", "Trident Throwing"],
    "John Constantine":      ["Exorcising", "Spell Casting"],
    "Doctor Fate":           ["Spell Casting", "Flying", "Portal Opening"],
    "Hawkgirl":              ["Mace Swinging", "Flying", "Wing Slashing"],
    "Mister Terrific":       ["T-Sphere Deploying", "Force Field Generating"],
    "Metamorpho":            ["Elemental Transforming", "Shape-Shifting"],
    "Krypto":                ["Flying", "Heat Vision Blasting", "Pouncing"],

    # --------------------------- VILLAINS ---------------------------
    "Lex Luthor":            ["Mech Suit Punching", "Strategizing", "Tech Deploying"],
    "General Zod":           ["Heat Vision Blasting", "Flying", "Punching"],
    "Doomsday":              ["Smashing", "Bone Spike Impaling", "Roaring"],
    "The Joker":             ["Gun Shooting", "Knife Slashing", "Gas Bombing"],
    "Bane":                  ["Venom-Fueled Punching", "Smashing", "Back Breaking"],
    "Ra's al Ghul":          ["Sword Slashing", "Martial Arts Striking"],
    "Scarecrow":             ["Fear Toxin Spraying"],
    "Two-Face":              ["Coin Flipping", "Gun Shooting"],
    "Penguin":               ["Umbrella Gadget Deploying", "Gun Shooting"],
    "Riddler":               ["Trap Setting", "Gun Shooting"],
    "Catwoman":              ["Whip Lashing", "Claw Slashing", "Acrobatic Flipping"],
    "Deathstroke":           ["Sword Slashing", "Gun Shooting", "Enhanced Fighting"],
    "Darkseid":              ["Omega Beam Blasting", "Flying", "Punching"],
    "Steppenwolf":           ["Electro-Axe Swinging", "Portal Opening", "Flying"],
    "Ares":                  ["Sword Slashing", "Armor Forming", "Energy Blasting"],
    "Black Manta":           ["Laser Blasting", "Harpoon Firing", "Jet Suit Flying"],
    "Ocean Master":          ["Trident Throwing", "Water Manipulating"],
    "Enchantress":           ["Magic Blasting", "Portal Opening"],
    "Amanda Waller":         ["Strategizing", "Commanding"],
    "Circe":                 ["Spell Casting", "Transforming"],
    "Brainiac":              ["Tech Deploying", "Mind Controlling", "City Shrinking"],
    "Sinestro":              ["Fear Ring Constructing", "Flying"],
    "Solomon Grundy":        ["Smashing", "Regenerating"],
    "King Shark":            ["Biting", "Smashing"],
    "Mister Freeze":         ["Freeze Ray Blasting"],
    "Poison Ivy":            ["Vine Whipping", "Toxin Spraying"],
    "Killer Croc":           ["Biting", "Smashing"],
    "Clayface":              ["Shape-Shifting", "Punching"],
    "The Engineer":          ["Nanotech Whipping", "Flying", "Punching"],
    "Ultraman":              ["Heat Vision Blasting", "Flying", "Punching", "Smashing"],
}


def sanitize(name: str) -> str:
    """Strip characters that are invalid in folder names on Windows/macOS/Linux."""
    invalid = '<>:"/\\|?*'
    for ch in invalid:
        name = name.replace(ch, "")
    return name.strip()


def create_dc_folders(base_path: str) -> None:
    os.makedirs(base_path, exist_ok=True)
    total_chars = 0
    total_subfolders = 0

    for character, actions in CHARACTERS.items():
        char_folder = os.path.join(base_path, sanitize(character))
        os.makedirs(char_folder, exist_ok=True)
        total_chars += 1
        print(f"Created: {char_folder}")

        for action in actions:
            action_folder = os.path.join(char_folder, sanitize(action))
            os.makedirs(action_folder, exist_ok=True)
            total_subfolders += 1
            print(f"    Created: {action_folder}")

    print("\nDone!")
    print(f"Character folders created:  {total_chars}")
    print(f"Action subfolders created:  {total_subfolders}")
    print(f"Location: {os.path.abspath(base_path)}")


if __name__ == "__main__":
    destination = sys.argv[1] if len(sys.argv) > 1 else "DC_Characters"
    create_dc_folders(destination)