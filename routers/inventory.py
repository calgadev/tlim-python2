from typing import Optional

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.character import Character
from models.inventory import Inventory
from models.item import Item
from models.server_item_price import ServerItemPrice
from services.sale_decision_service import calculate_decisions, SaleDecision

router = APIRouter(prefix="/inventory", tags=["inventory"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def inventory(
    request: Request,
    user_id: int,
    character_id: int,
    decision_filter: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    character = db.query(Character).filter_by(
        id=character_id, user_id=user_id
    ).first()
    if not character:
        raise HTTPException(status_code=404, detail="Character not found.")

    decisions, passive_gold, gross_value = calculate_decisions(
        db=db,
        character_id=character_id,
        server_id=character.server_id
    )

    # Apply decision filter if provided.
    if decision_filter:
        decisions = [d for d in decisions if d.decision.name == decision_filter]

    # Apply sorting.
    if sort_by == "value":
        decisions.sort(key=lambda d: d.estimated_value, reverse=True)
    elif sort_by == "name":
        decisions.sort(key=lambda d: d.item_name)
    else:
        # Default: sort by decision priority — items needing action first.
        priority = {
            SaleDecision.SELL_NPC: 0,
            SaleDecision.SELL_MARKET: 1,
            SaleDecision.NO_PRICE: 2,
            SaleDecision.KEEP: 3,
        }
        decisions.sort(key=lambda d: priority[d.decision])

    return templates.TemplateResponse("inventory.html", {
        "request": request,
        "character": character,
        "decisions": decisions,
        "passive_gold": passive_gold,
        "gross_value": gross_value,
        "decision_filter": decision_filter,
        "sort_by": sort_by,
        "sale_decisions": SaleDecision,
        "user_id": user_id,
        "character_id": character_id,
    })


@router.post("/{item_id}/goal", response_class=RedirectResponse)
def update_goal(
    item_id: int,
    user_id: int = Form(...),
    character_id: int = Form(...),
    goal_quantity: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    entry = db.query(Inventory).filter_by(
        character_id=character_id,
        item_id=item_id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Inventory entry not found.")

    # Empty string means the user wants to clear the goal.
    if not goal_quantity or not goal_quantity.strip():
        entry.goal_quantity = None
    else:
        try:
            entry.goal_quantity = int(goal_quantity.strip())
        except ValueError:
            raise HTTPException(status_code=422, detail="Goal must be a valid integer.")

    db.commit()

    return RedirectResponse(
        url=f"/inventory/?user_id={user_id}&character_id={character_id}",
        status_code=303
    )