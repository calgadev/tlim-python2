from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class ServerItemPrice(Base):
    __tablename__ = "server_item_prices"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    server_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("servers.id", ondelete="RESTRICT"), nullable=False
    )
    item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("items.id", ondelete="CASCADE"), nullable=False
    )

    # Manually entered by the user in Stage 1.
    # NULL means the price has not been registered yet for this server.
    # A future improvement could calculate a suggested price based on
    # the average across servers that already have a price for this item.
    market_price: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # The same item can only have one price per server.
    __table_args__ = (
        UniqueConstraint("server_id", "item_id", name="uq_server_item_price"),
    )

    server: Mapped["Server"] = relationship("Server", back_populates="item_prices")
    item: Mapped["Item"] = relationship("Item", back_populates="server_prices")

    def __repr__(self):
        return (
            f"<ServerItemPrice server_id={self.server_id} "
            f"item_id={self.item_id} market_price={self.market_price}>"
        )