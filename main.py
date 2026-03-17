from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine, Base
import models  # ensures all models are registered with Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TLIM - Tibia Loot & Inventory Manager")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return {"status": "TLIM is running"}