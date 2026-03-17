from datetime import datetime

from sqlalchemy import Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class HuntSession(Base):
    __tablename__ = "hunt_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    character_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("characters.id", ondelete="CASCADE"), nullable=False
    )

    # User-defined session name. Always required at the database level.
    # If the user leaves it blank, the router generates a default name
    # based on the import timestamp — e.g. "Hunt 17/03 18:11".
    name: Mapped[str] = mapped_column(Text, nullable=False)

    location: Mapped[str | None] = mapped_column(Text, nullable=True)

    # is_party defaults to False — most hunts are solo.
    # Ally level fields should only be displayed when is_party = TRUE.
    is_party: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Dates extracted from the Hunt Analyser log.
    # The parser is responsible for converting the text format
    # "2026-01-23, 18:24:04" to DateTime before persisting.
    session_start: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    session_end: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Duration as extracted from the log — e.g. "00:04h".
    # Stored as text since it is only used for display purposes.
    duration: Mapped[str] = mapped_column(Text, nullable=False)

    raw_xp: Mapped[int] = mapped_column(Integer, nullable=False)
    xp_with_bonus: Mapped[int] = mapped_column(Integer, nullable=False)
    loot_total: Mapped[int] = mapped_column(Integer, nullable=False)
    supplies: Mapped[int] = mapped_column(Integer, nullable=False)

    # balance is not stored — it is always calculated as loot_total - supplies.
    # Since both values are historical and never change after import,
    # there is no risk of divergence.

    damage: Mapped[int] = mapped_column(Integer, nullable=False)
    healing: Mapped[int] = mapped_column(Integer, nullable=False)

    # Character and ally levels at the time of the hunt — all optional.
    char_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ally_ek_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ally_ms_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ally_ed_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ally_rp_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ally_em_level: Mapped[int | None] = mapped_column(Integer, nullable=True)

    character: Mapped["Character"] = relationship(
        "Character", back_populates="hunt_sessions"
    )
    items: Mapped[list["HuntSessionItem"]] = relationship(
        "HuntSessionItem", back_populates="session", passive_deletes=True
    )
    monsters: Mapped[list["HuntSessionMonster"]] = relationship(
        "HuntSessionMonster", back_populates="session", passive_deletes=True
    )

    def __repr__(self):
        return (
            f"<HuntSession id={self.id} name={self.name!r} "
            f"character_id={self.character_id}>"
        )