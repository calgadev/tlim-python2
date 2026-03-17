from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Creature(Base):
    __tablename__ = "creatures"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Stored in lowercase — "rotworm", not "Rotworm".
    # Uniqueness may need to be revisited in Stage 2 if the TibiaWiki
    # scraping reveals naming conflicts between creature variants.
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    hunt_session_monsters: Mapped[list["HuntSessionMonster"]] = relationship(
        "HuntSessionMonster", back_populates="creature", passive_deletes=True
    )

    def __repr__(self):
        return f"<Creature id={self.id} name={self.name!r}>"