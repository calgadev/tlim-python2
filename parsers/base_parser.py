from dataclasses import dataclass
from datetime import datetime


@dataclass
class ParsedItem:
    # Represents a single item entry from the hunt log.
    # Name is stored without article — "gold coin", not "a gold coin".
    # The parser is responsible for stripping the article before creating this object.
    name: str
    quantity: int


@dataclass
class ParsedMonster:
    # Represents a single monster entry from the hunt log.
    name: str
    quantity: int


@dataclass
class ParsedHunt:
    # Represents a fully parsed hunt session — regardless of the source format.
    # Both text_hunt_parser and json_hunt_parser produce this same object.
    # User-defined fields (name, location, is_party, notes, ally levels)
    # are not included here — they arrive separately in the import service.

    session_start: datetime
    session_end: datetime

    # Duration string as extracted from the log — e.g. "00:04h", "01:30h".
    # Stored as-is since it is only used for display purposes.
    duration: str

    raw_xp: int
    xp_with_bonus: int
    loot_total: int
    supplies: int
    damage: int
    healing: int

    items: list[ParsedItem]
    monsters: list[ParsedMonster]