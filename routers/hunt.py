from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.character import Character
from models.hunt_session import HuntSession
from models.user import User
from parsers.json_hunt_parser import parse_json_hunt
from parsers.text_hunt_parser import parse_text_hunt
from services.hunt_import_service import import_hunt

router = APIRouter(prefix="/hunt", tags=["hunt"])
templates = Jinja2Templates(directory="templates")


def parse_optional_int(value: Optional[str]) -> Optional[int]:
    # HTML forms send empty strings for unfilled number fields.
    # This converts them to None instead of raising a parsing error.
    if not value or not value.strip():
        return None
    try:
        return int(value.strip())
    except ValueError:
        return None


@router.get("/", response_class=HTMLResponse)
def hunt_import_form(
    request: Request,
    user_id: int,
    character_id: int,
    error: Optional[str] = None,
    db: Session = Depends(get_db)
):
    character = db.query(Character).filter_by(
        id=character_id, user_id=user_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found.")

    return templates.TemplateResponse("hunt_import.html", {
        "request": request,
        "character": character,
        "user_id": user_id,
        "character_id": character_id,
        "message": error,
        "message_type": "danger" if error else None,
    })


@router.post("/", response_class=RedirectResponse)
async def import_hunt_route(
    user_id: int = Form(...),
    character_id: int = Form(...),
    name: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    is_party: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    char_level: Optional[str] = Form(None),
    ally_ek_level: Optional[str] = Form(None),
    ally_ms_level: Optional[str] = Form(None),
    ally_ed_level: Optional[str] = Form(None),
    ally_rp_level: Optional[str] = Form(None),
    ally_em_level: Optional[str] = Form(None),
    raw_text: Optional[str] = Form(None),
    json_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    base_url = f"/hunt/?user_id={user_id}&character_id={character_id}"

    has_text = raw_text and raw_text.strip()
    has_file = json_file and json_file.filename

    if not has_text and not has_file:
        return RedirectResponse(
            url=f"{base_url}&error=Please+provide+a+hunt+log+-+either+paste+the+text+or+upload+a+JSON+file.",
            status_code=303
        )

    try:
        if has_file:
            content = await json_file.read()
            parsed_hunt = parse_json_hunt(content.decode("utf-8"))
        else:
            parsed_hunt = parse_text_hunt(raw_text)
    except ValueError as e:
        return RedirectResponse(
            url=f"{base_url}&error={str(e)}",
            status_code=303
        )

    session_name = name.strip() if name and name.strip() else \
        f"Hunt {datetime.now().strftime('%d/%m %H:%M')}"

    is_party_bool = is_party == "on"

    try:
        session = import_hunt(
            db=db,
            parsed_hunt=parsed_hunt,
            character_id=character_id,
            name=session_name,
            location=location or None,
            is_party=is_party_bool,
            notes=notes or None,
            char_level=parse_optional_int(char_level),
            ally_ek_level=parse_optional_int(ally_ek_level),
            ally_ms_level=parse_optional_int(ally_ms_level),
            ally_ed_level=parse_optional_int(ally_ed_level),
            ally_rp_level=parse_optional_int(ally_rp_level),
            ally_em_level=parse_optional_int(ally_em_level),
        )
    except ValueError as e:
        return RedirectResponse(
            url=f"{base_url}&error={str(e)}",
            status_code=303
        )

    return RedirectResponse(
        url=f"/hunt/{session.id}?user_id={user_id}&character_id={character_id}",
        status_code=303
    )


@router.get("/history", response_class=HTMLResponse)
def hunt_history(
    request: Request,
    user_id: int,
    character_id: int,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    character = db.query(Character).filter_by(
        id=character_id, user_id=user_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found.")

    query = db.query(HuntSession).filter_by(character_id=character_id)

    if location:
        query = query.filter(HuntSession.location.ilike(f"%{location}%"))

    sessions = query.order_by(HuntSession.session_start.desc()).all()

    return templates.TemplateResponse("hunt_history.html", {
        "request": request,
        "character": character,
        "sessions": sessions,
        "location_filter": location,
        "user_id": user_id,
        "character_id": character_id,
    })


@router.get("/{hunt_id}", response_class=HTMLResponse)
def hunt_detail(
    request: Request,
    hunt_id: int,
    user_id: int,
    character_id: int,
    db: Session = Depends(get_db)
):
    session = db.query(HuntSession).filter_by(
        id=hunt_id, character_id=character_id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Hunt session not found.")

    balance = session.loot_total - session.supplies

    return templates.TemplateResponse("hunt_detail.html", {
        "request": request,
        "session": session,
        "balance": balance,
        "user_id": user_id,
        "character_id": character_id,
    })