from sqlalchemy import Integer, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Stored without article — "gold coin", not "a gold coin".
    # The parser is responsible for stripping the article on import.
    # Uniqueness may need to be revisited in Stage 2 if the TibiaWiki
    # scraping reveals items with different IDs sharing the same name
    # (e.g. togglable items like magic light wand).
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    # Explicit flag to avoid ambiguity — npc_price = 0 could mean either
    # "no NPC buys this item" or "an NPC buys it for 0 gold".
    npc_buyable: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # NULL when npc_buyable = FALSE — the absence of a value is intentional.
    npc_price: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Flag indicating this item can be delivered in a weekly task.
    # When TRUE, the interface should alert the user before recommending a sale.
    # The sale decision engine treats this item normally — the final call is always
    # the user's.
    is_task_item: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    # npc_seller is intentionally absent in Stage 1.
    # A single item can have multiple NPC buyers (some with limited availability),
    # which requires a separate item_npc_prices table.
    # This will be implemented in Stage 2 alongside TibiaWiki scraping.

    server_prices: Mapped[list["ServerItemPrice"]] = relationship(
        "ServerItemPrice", back_populates="item", passive_deletes=True
    )
    inventory_entries: Mapped[list["Inventory"]] = relationship(
        "Inventory", back_populates="item", passive_deletes=True
    )
    hunt_session_items: Mapped[list["HuntSessionItem"]] = relationship(
        "HuntSessionItem", back_populates="item", passive_deletes=True
    )

    def __repr__(self):
        return f"<Item id={self.id} name={self.name!r} npc_buyable={self.npc_buyable}>"