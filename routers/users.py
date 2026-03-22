from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.user_schema import UserCreate

router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    # Fetch all users to display on the selection screen.
    users = db.query(User).order_by(User.name).all()
    return templates.TemplateResponse(
        "users.html", {"request": request, "users": users}
    )


@router.post("/", response_class=RedirectResponse)
def create_user(name: str = Form(...), db: Session = Depends(get_db)):
    # Validate the input using the schema.
    try:
        validated = UserCreate(name=name)
    except ValueError as e:
        # For now, redirect back to the list on error.
        # Error feedback will be improved when we build the template.
        raise HTTPException(status_code=422, detail=str(e))

    # Check if the name is already taken before trying to insert.
    existing = db.query(User).filter_by(name=validated.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Name already taken.")

    user = User(name=validated.name)
    db.add(user)
    db.commit()

    # POST/Redirect/GET pattern — redirect after successful creation.
    return RedirectResponse(url="/users/", status_code=303)


@router.get("/{user_id}", response_class=RedirectResponse)
def select_user(user_id: int, db: Session = Depends(get_db)):
    # Verify the user exists before redirecting.
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    # Redirect to the character list for this user.
    return RedirectResponse(url=f"/characters/?user_id={user_id}", status_code=303)