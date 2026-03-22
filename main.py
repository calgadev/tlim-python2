from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine, Base
import models

from routers import users, characters

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TLIM - Tibia Loot & Inventory Manager")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(users.router)
app.include_router(characters.router)

@app.get("/")
def root():
    return {"status": "TLIM is running"}