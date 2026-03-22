import re
from datetime import datetime

from parsers.base_parser import ParsedHunt, ParsedItem, ParsedMonster


def parse_int(value: str) -> int:
    # Remove thousands separators and convert to integer.
    # Examples: "1,413" → 1413, "30" → 30, "0" → 0
    return int(value.replace(",", ""))


def parse_date(value: str) -> datetime:
    # Convert date string from Hunt Analyser text format to datetime.
    # Expected format: "2026-03-16, 17:14:36"
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


def parse_text_hunt(raw_text: str) -> ParsedHunt:
    # Entry point for text format parsing.
    # Receives the raw text pasted by the user and returns a ParsedHunt.

    # These will be populated as we read through the lines.
    session_start = None
    session_end = None
    duration = None
    raw_xp = None
    xp_with_bonus = None
    loot_total = None
    supplies = None
    damage = None
    healing = None
    items = []
    monsters = []

    # Tracks which section we are currently reading.
    # None = header, "monsters" = reading monster lines, "items" = reading item lines
    current_section = None

    for line in raw_text.splitlines():
        stripped = line.strip()

        # --- Section headers ---
        # When we find a section header, we switch the current section.
        # This also implicitly ends the previous section (Option B decision).
        if stripped == "Killed Monsters:":
            current_section = "monsters"
            continue

        if stripped == "Looted Items:":
            current_section = "items"
            continue

        # --- Section content ---
        if current_section == "monsters":
            match = re.match(r"(\d+)x (.+)", stripped)
            if match:
                quantity = int(match.group(1))
                name = match.group(2).strip()
                monsters.append(ParsedMonster(name=name, quantity=quantity))
            continue

        if current_section == "items":
            match = re.match(r"(\d+)x (.+)", stripped)
            if match:
                quantity = int(match.group(1))
                name = strip_article(match.group(2).strip())
                items.append(ParsedItem(name=name, quantity=quantity))
            continue

        # --- Header fields ---
        # Each line follows the "Key: value" pattern.
        # Lines that don't match a known key are ignored silently.
        if stripped.startswith("Session data:"):
            # Special case — extract two dates from "From ... to ..." format.
            date_match = re.search(
                r"From (\d{4}-\d{2}-\d{2}, \d{2}:\d{2}:\d{2}) to (\d{4}-\d{2}-\d{2}, \d{2}:\d{2}:\d{2})",
                stripped
            )
            if date_match:
                session_start = parse_date(date_match.group(1))
                session_end = parse_date(date_match.group(2))

        elif stripped.startswith("Session:"):
            duration = stripped.split(":", 1)[1].strip()

        elif stripped.startswith("Raw XP Gain:"):
            raw_xp = parse_int(stripped.split(":", 1)[1].strip())

        elif stripped.startswith("XP Gain:"):
            xp_with_bonus = parse_int(stripped.split(":", 1)[1].strip())

        elif stripped.startswith("Loot:"):
            loot_total = parse_int(stripped.split(":", 1)[1].strip())

        elif stripped.startswith("Supplies:"):
            supplies = parse_int(stripped.split(":", 1)[1].strip())

        elif stripped.startswith("Damage:"):
            damage = parse_int(stripped.split(":", 1)[1].strip())

        elif stripped.startswith("Healing:"):
            healing = parse_int(stripped.split(":", 1)[1].strip())

        # All other lines (Raw XP/h, XP/h, Damage/h, Healing/h, Balance)
        # are ignored silently.

    # Validate that all required fields were found before returning.
    missing = [
        name for name, value in [
            ("Session data", session_start),
            ("Session", duration),
            ("Raw XP Gain", raw_xp),
            ("XP Gain", xp_with_bonus),
            ("Loot", loot_total),
            ("Supplies", supplies),
            ("Damage", damage),
            ("Healing", healing),
        ]
        if value is None
    ]
    if missing:
        raise ValueError(
            f"Could not parse the following fields from the hunt log: {', '.join(missing)}."
        )

    return ParsedHunt(
        session_start=session_start,
        session_end=session_end,
        duration=duration,
        raw_xp=raw_xp,
        xp_with_bonus=xp_with_bonus,
        loot_total=loot_total,
        supplies=supplies,
        damage=damage,
        healing=healing,
        items=items,
        monsters=monsters
    )