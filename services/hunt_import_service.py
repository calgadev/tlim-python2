from datetime import datetime
from sqlalchemy.orm import Session

from models.character import Character
from models.creature import Creature
from models.hunt_session import HuntSession
from models.hunt_session_item import HuntSessionItem
from models.hunt_session_monster import HuntSessionMonster
from models.inventory import Inventory
from models.item import Item
from parsers.base_parser import ParsedHunt


def import_hunt(
    db: Session,
    parsed_hunt: ParsedHunt,
    character_id: int,
    name: str,
    location: str | None,
    is_party: bool,
    notes: str | None,
    char_level: int | None,
    ally_ek_level: int | None,
    ally_ms_level: int | None,
    ally_ed_level: int | None,
    ally_rp_level: int | None,
    ally_em_level: int | None,
) -> HuntSession:
    try:
        # --- Step 1: Validate creatures ---
        # Collect all missing creatures before failing so the user can fix
        # everything at once instead of discovering problems one by one.
        missing_creatures = []
        creature_map = {}  # name → Creature object, reused in step 4

        for parsed_monster in parsed_hunt.monsters:
            creature = db.query(Creature).filter_by(name=parsed_monster.name).first()
            if not creature:
                missing_creatures.append(parsed_monster.name)
            else:
                creature_map[parsed_monster.name] = creature

        # --- Step 2: Validate items ---
        missing_items = []
        item_map = {}  # name → Item object, reused in steps 5 and 6

        for parsed_item in parsed_hunt.items:
            item = db.query(Item).filter_by(name=parsed_item.name).first()
            if not item:
                missing_items.append(parsed_item.name)
            else:
                item_map[parsed_item.name] = item

        # Fail with a combined message if anything is missing.
        if missing_creatures or missing_items:
            error_parts = []
            if missing_creatures:
                error_parts.append(f"Unknown creatures: {', '.join(missing_creatures)}")
            if missing_items:
                error_parts.append(f"Unknown items: {', '.join(missing_items)}")
            raise ValueError(" | ".join(error_parts))

        # --- Step 3: Persist HuntSession ---
        session = HuntSession(
            character_id=character_id,
            name=name,
            location=location,
            is_party=is_party,
            notes=notes,
            session_start=parsed_hunt.session_start,
            session_end=parsed_hunt.session_end,
            duration=parsed_hunt.duration,
            raw_xp=parsed_hunt.raw_xp,
            xp_with_bonus=parsed_hunt.xp_with_bonus,
            loot_total=parsed_hunt.loot_total,
            supplies=parsed_hunt.supplies,
            damage=parsed_hunt.damage,
            healing=parsed_hunt.healing,
            char_level=char_level,
            ally_ek_level=ally_ek_level,
            ally_ms_level=ally_ms_level,
            ally_ed_level=ally_ed_level,
            ally_rp_level=ally_rp_level,
            ally_em_level=ally_em_level,
        )
        db.add(session)
        db.flush()  # sends the INSERT to the database without committing,
                    # so session.id is available for the foreign keys below

        # --- Step 4: Persist HuntSessionMonster ---
        for parsed_monster in parsed_hunt.monsters:
            creature = creature_map[parsed_monster.name]
            db.add(HuntSessionMonster(
                session_id=session.id,
                creature_id=creature.id,
                quantity=parsed_monster.quantity
            ))

        # --- Step 5: Persist HuntSessionItem ---
        for parsed_item in parsed_hunt.items:
            item = item_map[parsed_item.name]
            db.add(HuntSessionItem(
                session_id=session.id,
                item_id=item.id,
                quantity=parsed_item.quantity
            ))

        # --- Step 6: Update inventory ---
        for parsed_item in parsed_hunt.items:
            item = item_map[parsed_item.name]

            inventory_entry = db.query(Inventory).filter_by(
                character_id=character_id,
                item_id=item.id
            ).first()

            if inventory_entry:
                # Item already exists in inventory — add to current quantity.
                inventory_entry.quantity += parsed_item.quantity
            else:
                # First time this item appears for this character — create the entry.
                # goal_quantity starts as NULL — user can set a goal manually later.
                db.add(Inventory(
                    character_id=character_id,
                    item_id=item.id,
                    quantity=parsed_item.quantity,
                    goal_quantity=None
                ))

        # --- Step 7: Commit ---
        # All steps succeeded — persist everything to the database.
        db.commit()
        return session

    except Exception:
        # Something went wrong — roll back everything so no partial data is saved.
        db.rollback()
        raise