from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine, Base
import models

from routers import inventory, users, characters, hunt, items

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TLIM - Tibia Loot & Inventory Manager")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(characters.router)
app.include_router(hunt.router)
app.include_router(inventory.router)
app.include_router(items.router)

@app.get("/")
def root():
    return {"status": "TLIM is running"}