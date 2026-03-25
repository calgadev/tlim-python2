from typing import Optional

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.character import Character
from models.item import Item
from models.server_item_price import ServerItemPrice

router = APIRouter(prefix="/items", tags=["items"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def list_items(
    request: Request,
    user_id: int,
    character_id: int,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    character = db.query(Character).filter_by(
        id=character_id, user_id=user_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found.")

    # Base query — all items ordered alphabetically.
    query = db.query(Item).order_by(Item.name)

    # Apply name filter if provided.
    if search:
        query = query.filter(Item.name.ilike(f"%{search}%"))

    items = query.all()

    # Fetch market prices for this server — build a dict for quick lookup.
    # { item_id: ServerItemPrice } 
    price_entries = db.query(ServerItemPrice).filter_by(
        server_id=character.server_id
    ).all()
    prices = {p.item_id: p for p in price_entries}

    return templates.TemplateResponse("items.html", {
        "request": request,
        "character": character,
        "items": items,
        "prices": prices,
        "search": search,
        "user_id": user_id,
        "character_id": character_id,
    })


@router.post("/{item_id}/price", response_class=RedirectResponse)
def update_price(
    item_id: int,
    user_id: int = Form(...),
    character_id: int = Form(...),
    market_price: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    character = db.query(Character).filter_by(
        id=character_id, user_id=user_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found.")

    item = db.query(Item).filter_by(id=item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")

    # Convert price — empty string means the user wants to clear the price.
    if not market_price or not market_price.strip():
        price_value = None
    else:
        try:
            price_value = int(market_price.strip())
        except ValueError:
            raise HTTPException(status_code=422, detail="Price must be a valid integer.")

    # Update existing entry or create a new one.
    entry = db.query(ServerItemPrice).filter_by(
        server_id=character.server_id,
        item_id=item_id
    ).first()

    if entry:
        entry.market_price = price_value
    else:
        entry = ServerItemPrice(
            server_id=character.server_id,
            item_id=item_id,
            market_price=price_value
        )
        db.add(entry)

    db.commit()

    return RedirectResponse(
        url=f"/items/?user_id={user_id}&character_id={character_id}",
        status_code=303
    )