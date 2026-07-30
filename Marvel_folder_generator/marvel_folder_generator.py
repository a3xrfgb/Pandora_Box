#!/usr/bin/env python3
"""
Marvel Character Folder Generator
==================================
Creates one main folder per Marvel hero/villain (spanning Iron Man (2008)
through the Avengers: Doomsday era) and, inside each, subfolders for that
character's OWN signature action scenes only.

No action subfolder is shared across characters unless it genuinely
matches both (e.g. "Flying" only appears for characters who actually fly).
Spider-Man gets "Web Shooting," Thor does not. Thor gets "Mjolnir
Throwing," Captain America does not. Etc.

USAGE
-----
    python marvel_folder_generator.py                # creates ./Marvel_Characters
    python marvel_folder_generator.py "D:/MyFolder"  # creates in a custom path

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
    "Iron Man":            ["Repulsor Blasting", "Unibeam Firing", "Flying", "Landing", "Suit Up"],
    "War Machine":         ["Minigun Firing", "Missile Launching", "Flying", "Landing"],
    "Captain America":     ["Shield Throwing", "Shield Blocking", "Punching", "Jumping"],
    "Falcon":               ["Flying", "Gliding", "Redwing Deploying", "Shooting"],
    "Black Widow":          ["Kicking", "Flipping", "Widow's Bite Shocking", "Shooting"],
    "Hawkeye":              ["Arrow Shooting", "Trick Shot Firing", "Aiming"],
    "Thor":                 ["Mjolnir Throwing", "Lightning Striking", "Stormbreaker Throwing", "Flying", "Smashing"],
    "Hulk":                 ["Smashing", "Roaring", "Jumping", "Punching", "Throwing", "Transforming"],
    "Doctor Strange":       ["Portal Opening", "Spell Casting", "Shielding", "Astral Projecting", "Time Looping"],
    "Spider-Man":           ["Web Shooting", "Wall Crawling", "Swinging", "Punching", "Dodging", "Landing"],
    "Black Panther":        ["Claw Slashing", "Vibranium Blocking", "Jumping", "Running", "Energy Absorbing"],
    "Ant-Man":              ["Shrinking", "Growing", "Punching", "Riding Ant"],
    "Wasp":                 ["Shrinking", "Flying", "Blasting", "Stinging"],
    "Scarlet Witch":        ["Hex Blasting", "Levitating", "Telekinesis", "Reality Warping"],
    "Vision":                ["Phasing", "Flying", "Energy Blasting", "Density Shifting"],
    "Quicksilver":           ["Super Speed Running"],
    "Star-Lord":             ["Blaster Firing", "Jet Boot Flying", "Dodging"],
    "Gamora":                ["Sword Slashing", "Flipping", "Dodging"],
    "Drax":                  ["Stabbing", "Throwing", "Smashing"],
    "Rocket Raccoon":        ["Gun Shooting", "Gadget Throwing"],
    "Groot":                 ["Growing", "Smashing", "Regenerating", "Vine Whipping"],
    "Nebula":                ["Cybernetic Punching", "Throwing", "Blade Slashing"],
    "Mantis":                ["Touch Sedating", "Empathic Sensing"],
    "Yondu":                 ["Whistling Arrow Controlling", "Flying Arrow Shooting"],
    "Captain Marvel":        ["Photon Blasting", "Flying", "Punching"],
    "Shang-Chi":             ["Martial Arts Striking", "Blocking", "Ten Rings Wielding"],
    "Wolverine":             ["Claw Slashing", "Healing", "Jumping"],
    "Deadpool":              ["Sword Slashing", "Shooting", "Regenerating"],
    "Winter Soldier":        ["Metal Arm Punching", "Shooting", "Throwing"],
    "Valkyrie":              ["Sword Slashing", "Pegasus Flying", "Blocking"],
    "Okoye":                 ["Spear Throwing", "Blocking", "Jumping"],
    "Nick Fury":             ["Commanding", "Shooting"],
    "Yelena Belova":         ["Kicking", "Gymnastics Flipping", "Shooting"],
    "Red Guardian":          ["Punching", "Shield Bashing"],

    # --------------------------- VILLAINS ---------------------------
    "Iron Monger":           ["Repulsor Blasting", "Smashing", "Flying"],
    "Whiplash":               ["Whip Lashing", "Electrocuting"],
    "Abomination":            ["Smashing", "Roaring", "Jumping", "Punching"],
    "Loki":                   ["Illusion Casting", "Dagger Throwing", "Teleporting", "Scepter Blasting"],
    "Red Skull":               ["Punching", "Shooting", "Cube Wielding"],
    "Aldrich Killian":         ["Fire Breathing", "Regenerating", "Punching"],
    "Malekith":                ["Dark Energy Blasting", "Sword Slashing"],
    "Ronan the Accuser":       ["Hammer Smashing", "Flying"],
    "Ultron":                  ["Flying", "Energy Blasting", "Transforming", "Drone Swarming"],
    "Yellowjacket":            ["Shrinking", "Blasting", "Flying"],
    "Zemo":                    ["Strategizing", "Manipulating"],
    "Vulture":                  ["Flying", "Diving", "Claw Slashing"],
    "Hela":                     ["Blade Summoning", "Throwing", "Resurrecting Undead"],
    "Grandmaster":              ["Energy Blasting"],
    "Thanos":                   ["Snapping", "Punching", "Blocking", "Gauntlet Blasting", "Throwing"],
    "Ghost":                    ["Phasing", "Punching", "Teleporting"],
    "Ego":                      ["Energy Blasting", "Transforming", "Planet Forming"],
    "Mysterio":                 ["Illusion Casting", "Drone Controlling", "Smoke Screening"],
    "Taskmaster":                ["Mimicking", "Shield Throwing", "Bow Shooting", "Sword Slashing"],
    "Killmonger":                ["Spear Throwing", "Claw Slashing", "Punching"],
    "Gorr the God Butcher":      ["Shadow Blade Slashing", "Portal Opening"],
    "Namor":                     ["Flying", "Trident Throwing", "Punching", "Water Summoning"],
    "Kang the Conqueror":        ["Time Manipulating", "Energy Blasting", "Punching"],
    "High Evolutionary":         ["Gene Splicing", "Blasting", "Mutating Creatures"],
    "The Mandarin (Wenwu)":      ["Ring Blasting", "Punching", "Energy Whipping"],
    "Ikaris":                    ["Flying", "Eye Beam Blasting", "Punching"],
    "Sersi":                     ["Transmuting", "Transforming"],
    "Dar-Benn":                  ["Hammer Smashing", "Portal Opening"],
    "Cassandra Nova":            ["Telekinetic Blasting", "Mind Controlling"],
    "The Void":                  ["Void Consuming", "Energy Blasting", "Flying"],
    "Doctor Doom":               ["Energy Blasting", "Armor Smashing", "Sorcery Casting"],
}


def sanitize(name: str) -> str:
    """Strip characters that are invalid in folder names on Windows/macOS/Linux."""
    invalid = '<>:"/\\|?*'
    for ch in invalid:
        name = name.replace(ch, "")
    return name.strip()


def create_marvel_folders(base_path: str) -> None:
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
    destination = sys.argv[1] if len(sys.argv) > 1 else "Marvel_Characters"
    create_marvel_folders(destination)