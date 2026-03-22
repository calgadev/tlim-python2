from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HuntImportForm(BaseModel):
    # User-defined fields from the import form.
    # At least one of raw_text or json_content must be provided —
    # this is validated in the router, not here.
    name: Optional[str] = None
    location: Optional[str] = None
    is_party: bool = False
    notes: Optional[str] = None
    char_level: Optional[int] = None
    ally_ek_level: Optional[int] = None
    ally_ms_level: Optional[int] = None
    ally_ed_level: Optional[int] = None
    ally_rp_level: Optional[int] = None
    ally_em_level: Optional[int] = None


class HuntSessionResponse(BaseModel):
    # Output schema for hunt session listing and detail.
    id: int
    name: str
    location: Optional[str] = None
    is_party: bool
    session_start: datetime
    session_end: datetime
    duration: str
    raw_xp: int
    xp_with_bonus: int
    loot_total: int
    supplies: int
    damage: int
    healing: int
    char_level: Optional[int] = None

    model_config = {"from_attributes": True}