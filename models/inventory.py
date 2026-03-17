from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False
    )
    item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("items.id", ondelete="RESTRICT"), nullable=False
    )

    # Current stock — updated exclusively via hunt import in Stage 1.
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # User-defined stock goal. NULL means no goal is set —
    # the sale decision engine treats this as goal = 0,
    # making the full quantity available for sale.
    goal_quantity: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # The same item can only appear once per character.
    __table_args__ = (
        UniqueConstraint("character_id", "item_id", name="uq_inventory_character_item"),
    )

    character: Mapped["Character"] = relationship("Character", back_populates="inventory")
    item: Mapped["Item"] = relationship("Item", back_populates="inventory_entries")

    def __repr__(self):
        return (
            f"<Inventory character_id={self.character_id} "
            f"item_id={self.item_id} quantity={self.quantity} "
            f"goal_quantity={self.goal_quantity}>"
        )