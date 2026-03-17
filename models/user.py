from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)

    # A user can have multiple characters.
    # This list is populated automatically by SQLAlchemy when you access
    # user.characters — no manual query needed.
    characters: Mapped[list["Character"]] = relationship(
        "Character", back_populates="user"
    )

    def __repr__(self):
        return f"<User id={self.id} name={self.name!r}>"