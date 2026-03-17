from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class HuntSessionMonster(Base):
    __tablename__ = "hunt_session_monsters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("hunt_sessions.id", ondelete="CASCADE"), nullable=False
    )
    creature_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("creatures.id", ondelete="RESTRICT"), nullable=False
    )

    # Total killed in this session.
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # The same creature can only appear once per session.
    __table_args__ = (
        UniqueConstraint("session_id", "creature_id", name="uq_hunt_session_monster"),
    )

    session: Mapped["HuntSession"] = relationship(
        "HuntSession", back_populates="monsters"
    )
    creature: Mapped["Creature"] = relationship(
        "Creature", back_populates="hunt_session_monsters"
    )

    def __repr__(self):
        return (
            f"<HuntSessionMonster session_id={self.session_id} "
            f"creature_id={self.creature_id} quantity={self.quantity}>"
        )