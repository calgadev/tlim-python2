from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class HuntSessionItem(Base):
    __tablename__ = "hunt_session_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("hunt_sessions.id", ondelete="CASCADE"), nullable=False
    )
    item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("items.id", ondelete="RESTRICT"), nullable=False
    )

    # Total collected in this session.
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # The same item can only appear once per session.
    __table_args__ = (
        UniqueConstraint("session_id", "item_id", name="uq_hunt_session_item"),
    )

    session: Mapped["HuntSession"] = relationship(
        "HuntSession", back_populates="items"
    )
    item: Mapped["Item"] = relationship(
        "Item", back_populates="hunt_session_items"
    )

    def __repr__(self):
        return (
            f"<HuntSessionItem session_id={self.session_id} "
            f"item_id={self.item_id} quantity={self.quantity}>"
        )