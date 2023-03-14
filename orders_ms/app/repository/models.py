import uuid
from typing import List
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def generate_uuid():
    return str(uuid.uuid4())


class Base(DeclarativeBase):
    pass


class Order(Base):
    __tablename__ = "order"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    user_id: Mapped[str] = mapped_column(String, nullable=False)
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )
    status: Mapped[str] = mapped_column(String(64), nullable=False, default="created")
    created_at: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now())
    schedule_id: Mapped[str] = mapped_column(String, nullable=True)
    delivery_id: Mapped[str] = mapped_column(String, nullable=True)

    def __repr__(self) -> str:
        return (
            f"Order(id={self.id!r}, user_id={self.user_id!r}, status={self.status!r},"
            f" schedule_id={self.schedule_id!r}, delivery_id={self.delivery_id!r})"
        )


class OrderItem(Base):
    __tablename__ = "order_item"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    order_id: Mapped[str] = mapped_column(ForeignKey("order.id"))
    product: Mapped[str] = mapped_column(String, nullable=False)
    size: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return (
            f"OrderItem(id={self.id!r}, order_id={self.order_id!r}, product={self.product!r},"
            f" size={self.size!r}, quantity={self.quantity!r})"
        )

    def dict(self):
        return {
            "product": self.product,
            "size": self.size,
            "quantity": self.quantity,
        }
