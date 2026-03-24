import enum
from dataclasses import dataclass

from sqlalchemy.orm import Session

from models.inventory import Inventory
from models.server_item_price import ServerItemPrice


class SaleDecision(enum.Enum):
    KEEP = "Keep"
    SELL_NPC = "Sell to NPC"
    SELL_MARKET = "Sell on market"
    NO_PRICE = "No price available"


@dataclass
class ItemDecision:
    # Represents the sale decision for a single inventory item.
    item_id: int
    item_name: str
    is_task_item: bool
    current_quantity: int
    goal_quantity: int | None
    surplus_quantity: int
    npc_buyable: bool
    npc_price: int | None
    market_price: int | None
    decision: SaleDecision
    estimated_value: int
    missing_market_price: bool  # True when npc_buyable but market_price is NULL


def calculate_decisions(
    db: Session,
    character_id: int,
    server_id: int
) -> tuple[list[ItemDecision], int, int]:
    # Returns a tuple of (decisions, passive_gold, gross_value).
    # passive_gold = sum of estimated_value for all items with surplus
    # gross_value = sum of (total quantity × best price) for all items

    inventory_entries = (
        db.query(Inventory)
        .filter_by(character_id=character_id)
        .all()
    )

    decisions = []
    passive_gold = 0
    gross_value = 0

    for entry in inventory_entries:
        item = entry.item

        # Fetch the market price for this item on the character's server.
        price_entry = db.query(ServerItemPrice).filter_by(
            server_id=server_id,
            item_id=item.id
        ).first()
        market_price = price_entry.market_price if price_entry else None

        # --- Step 1: Calculate surplus ---
        # If current quantity is below goal, keep everything.
        # If goal is NULL, the full quantity is available for sale.
        if entry.goal_quantity is not None and entry.current_quantity < entry.goal_quantity:
            surplus = 0
        elif entry.goal_quantity is not None:
            surplus = entry.current_quantity - entry.goal_quantity
        else:
            surplus = entry.current_quantity

        # --- Step 2: Determine sale decision ---
        missing_market_price = False

        if surplus == 0:
            decision = SaleDecision.KEEP
            selling_price = 0

        elif not item.npc_buyable and not market_price:
            # No NPC buyer and no market price — cannot recommend anything.
            decision = SaleDecision.NO_PRICE
            selling_price = 0

        elif not item.npc_buyable:
            # NPC does not buy this item — market is the only option.
            decision = SaleDecision.SELL_MARKET
            selling_price = market_price

        elif not market_price:
            # NPC buys but market price is unknown — fallback to NPC with warning.
            decision = SaleDecision.SELL_NPC
            selling_price = item.npc_price
            missing_market_price = True

        elif item.npc_price >= market_price:
            # NPC pays equal or more — prefer NPC (faster, no market fee).
            decision = SaleDecision.SELL_NPC
            selling_price = item.npc_price

        else:
            # Market pays more.
            decision = SaleDecision.SELL_MARKET
            selling_price = market_price

        # --- Step 3: Calculate values ---
        estimated_value = surplus * selling_price if selling_price else 0
        passive_gold += estimated_value

        # Gross value uses the full quantity, not just the surplus.
        item_gross = entry.current_quantity * selling_price if selling_price else 0
        gross_value += item_gross

        decisions.append(ItemDecision(
            item_id=item.id,
            item_name=item.name,
            is_task_item=item.is_task_item,
            current_quantity=entry.current_quantity,
            goal_quantity=entry.goal_quantity,
            surplus_quantity=surplus,
            npc_buyable=item.npc_buyable,
            npc_price=item.npc_price,
            market_price=market_price,
            decision=decision,
            estimated_value=estimated_value,
            missing_market_price=missing_market_price,
        ))

    return decisions, passive_gold, gross_value