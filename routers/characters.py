from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.character import Character, Vocation
from models.server import Server
from models.user import User
from schemas.character_schema import CharacterCreate, CharacterEdit

router = APIRouter(prefix="/characters", tags=["characters"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def list_characters(request: Request, user_id: int, db: Session = Depends(get_db)):
    # Verify the user exists before loading their characters.
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    characters = (
        db.query(Character)
        .filter_by(user_id=user_id)
        .order_by(Character.name)
        .all()
    )
    servers = db.query(Server).order_by(Server.name).all()
    vocations = [v for v in Vocation]

    return templates.TemplateResponse("characters.html", {
        "request": request,
        "user": user,
        "characters": characters,
        "servers": servers,
        "vocations": vocations,
        "user_id": user_id,
    })


@router.post("/", response_class=RedirectResponse)
def create_character(
    user_id: int = Form(...),
    name: str = Form(...),
    server_id: int = Form(...),
    vocation: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        validated = CharacterCreate(name=name, server_id=server_id, vocation=vocation)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Check for duplicate name for this user.
    existing = db.query(Character).filter_by(
        user_id=user_id, name=validated.name
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Character name already exists.")

    # Convert vocation string to Enum or None.
    vocation_enum = Vocation(validated.vocation) if validated.vocation else None

    character = Character(
        user_id=user_id,
        name=validated.name,
        server_id=validated.server_id,
        vocation=vocation_enum
    )
    db.add(character)
    db.commit()

    return RedirectResponse(url=f"/characters/?user_id={user_id}", status_code=303)


@router.get("/{character_id}", response_class=RedirectResponse)
def select_character(character_id: int, user_id: int, db: Session = Depends(get_db)):
    # Verify the character exists and belongs to the user.
    character = db.query(Character).filter_by(
        id=character_id, user_id=user_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found.")

    # Redirect to inventory with both user and character context.
    return RedirectResponse(
        url=f"/inventory/?user_id={user_id}&character_id={character_id}",
        status_code=303
    )


@router.get("/{character_id}/edit", response_class=HTMLResponse)
def edit_character_form(
    request: Request,
    character_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    character = db.query(Character).filter_by(
        id=character_id, user_id=user_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found.")

    servers = db.query(Server).order_by(Server.name).all()
    vocations = [v for v in Vocation]

    return templates.TemplateResponse("character_edit.html", {
        "request": request,
        "character": character,
        "servers": servers,
        "vocations": vocations,
        "user_id": user_id,
    })


@router.post("/{character_id}/edit", response_class=RedirectResponse)
def edit_character(
    character_id: int,
    user_id: int = Form(...),
    name: str = Form(...),
    server_id: int = Form(...),
    vocation: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    character = db.query(Character).filter_by(
        id=character_id, user_id=user_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found.")

    try:
        validated = CharacterEdit(name=name, server_id=server_id, vocation=vocation)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # Check for duplicate name — exclude the current character from the check.
    existing = db.query(Character).filter(
        Character.user_id == user_id,
        Character.name == validated.name,
        Character.id != character_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Character name already exists.")

    character.name = validated.name
    character.server_id = validated.server_id
    character.vocation = Vocation(validated.vocation) if validated.vocation else None
    db.commit()

    return RedirectResponse(url=f"/characters/?user_id={user_id}", status_code=303)