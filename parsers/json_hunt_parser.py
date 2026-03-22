import json
import re
from datetime import datetime

from parsers.base_parser import ParsedHunt, ParsedItem, ParsedMonster


def parse_int(value: str) -> int:
    # Remove thousands separators and convert to integer.
    # Examples: "1,479" → 1479, "31,183" → 31183, "-3,064" → -3064
    return int(value.replace(",", ""))


def parse_date(value: str) -> datetime:
    # Convert date string from Hunt Analyser JSON format to datetime.
    # Expected format: "2026-01-23, 18:24:04"
    try:
        return datetime.strptime(value, "%Y-%m-%d, %H:%M:%S")
    except ValueError:
        raise ValueError(
            f"Invalid date format: '{value}'. Expected format: 'YYYY-MM-DD, HH:MM:SS'."
        )


def strip_article(name: str) -> str:
    # Remove leading article from item name.
    # "a gold coin" → "gold coin"
    # "an obsidian lance" → "obsidian lance"
    # Names that don't start with an article are returned as-is.
    return re.sub(r"^(a|an) ", "", name.strip())


def parse_json_hunt(raw_json: str) -> ParsedHunt:
    # Entry point for JSON format parsing.
    # Receives the raw JSON string from the uploaded file and returns a ParsedHunt.
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {e}")

    # Parse items — strip article from each name before storing.
    items = [
        ParsedItem(
            name=strip_article(entry["Name"]),
            quantity=entry["Count"]
        )
        for entry in data.get("Looted Items", [])
    ]

    # Parse monsters.
    monsters = [
        ParsedMonster(
            name=entry["Name"],
            quantity=entry["Count"]
        )
        for entry in data.get("Killed Monsters", [])
    ]

    return ParsedHunt(
        session_start=parse_date(data["Session start"]),
        session_end=parse_date(data["Session end"]),
        duration=data["Session length"],
        raw_xp=parse_int(data["Raw XP Gain"]),
        xp_with_bonus=parse_int(data["XP Gain"]),
        loot_total=parse_int(data["Loot"]),
        supplies=parse_int(data["Supplies"]),
        damage=parse_int(data["Damage"]),
        healing=parse_int(data["Healing"]),
        items=items,
        monsters=monsters
    )