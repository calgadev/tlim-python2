import json
import models 
from pathlib import Path

from database import SessionLocal, engine, Base
from models.server import Server, ServerType
from models.item import Item
from models.creature import Creature

# Create all tables if they don't exist yet.
Base.metadata.create_all(bind=engine)

# Seed data is stored in JSON files to keep this script clean and easy to update.
# To add more servers, items or creatures, just edit the JSON files.
SEED_DATA_DIR = Path(__file__).parent / "seed_data"


def load_json(filename):
    with open(SEED_DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def seed_servers(db):
    data = load_json("servers.json")
    inserted = 0

    for entry in data:
        # Check if the server already exists before inserting.
        # This makes the seed safe to run multiple times.
        exists = db.query(Server).filter_by(name=entry["name"]).first()
        if exists:
            continue

        server = Server(
            name=entry["name"],
            type=ServerType(entry["type"])
        )
        db.add(server)
        inserted += 1

    db.commit()
    print(f"Servers: {inserted} inserted, {len(data) - inserted} already existed.")


def seed_items(db):
    data = load_json("items.json")
    inserted = 0

    for entry in data:
        exists = db.query(Item).filter_by(name=entry["name"]).first()
        if exists:
            continue

        item = Item(
            name=entry["name"],
            npc_buyable=entry["npc_buyable"],
            npc_price=entry["npc_price"],
            is_task_item=entry["is_task_item"]
        )
        db.add(item)
        inserted += 1

    db.commit()
    print(f"Items: {inserted} inserted, {len(data) - inserted} already existed.")


def seed_creatures(db):
    data = load_json("creatures.json")
    inserted = 0

    for entry in data:
        exists = db.query(Creature).filter_by(name=entry["name"]).first()
        if exists:
            continue

        creature = Creature(name=entry["name"])
        db.add(creature)
        inserted += 1

    db.commit()
    print(f"Creatures: {inserted} inserted, {len(data) - inserted} already existed.")


def run():
    db = SessionLocal()
    try:
        print("Starting seed...")
        seed_servers(db)
        seed_items(db)
        seed_creatures(db)
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    run()