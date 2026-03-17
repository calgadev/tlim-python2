import enum

from sqlalchemy import Integer, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ServerType(enum.Enum):
    OPTIONAL_PVP = "Optional PvP"
    OPEN_PVP = "Open PvP"
    RETRO_OPEN_PVP = "Retro Open PvP"
    RETRO_HARDCORE_PVP = "Retro Hardcore PvP"
    HARDCORE_PVP = "Hardcore PvP"


class Server(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    type: Mapped[ServerType] = mapped_column(Enum(ServerType), nullable=False)

    # Populated by SQLAlchemy when accessing server.characters.
    # passive_deletes=True tells SQLAlchemy to let the database enforce
    # the deletion rule — in this case, RESTRICT is the default SQLite
    # behavior when a foreign key is referenced.
    characters: Mapped[list["Character"]] = relationship(
        "Character", back_populates="server", passive_deletes=True
    )
    item_prices: Mapped[list["ServerItemPrice"]] = relationship(
        "ServerItemPrice", back_populates="server", passive_deletes=True
    )

    def __repr__(self):
        return f"<Server id={self.id} name={self.name!r} type={self.type}>"