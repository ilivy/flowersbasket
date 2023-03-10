from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.repository.models import Order, OrderItem
from app.web.api.schemas import OrderItemSchema


class OrdersRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, items: List[OrderItemSchema], user_id: UUID) -> Order:
        db_order = Order(items=[OrderItem(**item) for item in items], user_id=user_id)
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def get(self, order_id: UUID, **filters) -> Order:
        return (
            self.db.query(Order)
            .filter(Order.id == str(order_id))
            .filter_by(**filters)
            .first()
        )

    def list(self, skip: int = 1, limit: int = 100, **filters) -> List[Order]:
        return self.db.query(Order).filter_by(**filters).offset(skip).limit(limit).all()

    def update(self, order_id: UUID, **payload) -> Order:
        order = self.get(order_id)
        # Replace OrderItems
        if "items" in payload:
            # Remove old OrderItems
            for old_item in order.items:
                self.db.delete(old_item)
            # Set new OrderItems
            order.items = [OrderItem(**item) for item in payload.pop("items")]
        # Replace all the other Order properties, if there are any
        for key, value in payload.items():
            setattr(order, key, value)
        self.db.commit()
        return order

    def delete(self, order_id: UUID) -> None:
        self.db.delete(self.get(order_id))
        self.db.commit()
