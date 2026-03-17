import enum

from sqlalchemy import Integer, Text, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Vocation(enum.Enum):
    EK = "EK"
    MS = "MS"
    ED = "ED"
    RP = "RP"
    EM = "EM"


class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    server_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("servers.id", ondelete="RESTRICT"), nullable=False
    )
    # Vocation is optional — a character without one is a Rookie from Rookgaard.
    # Rookgaard characters have restricted NPC access and limited functionality.
    vocation: Mapped[Vocation | None] = mapped_column(Enum(Vocation), nullable=True)

    # Uniqueness enforced at the database level — same user cannot have
    # two characters with the same name, but different users can.
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_character_user_name"),
    )

    user: Mapped["User"] = relationship("User", back_populates="characters")
    server: Mapped["Server"] = relationship("Server", back_populates="characters")
    inventory: Mapped[list["Inventory"]] = relationship(
        "Inventory", back_populates="character", passive_deletes=True
    )
    hunt_sessions: Mapped[list["HuntSession"]] = relationship(
        "HuntSession", back_populates="character", passive_deletes=True
    )

    def __repr__(self):
        return f"<Character id={self.id} name={self.name!r} vocation={self.vocation}>"