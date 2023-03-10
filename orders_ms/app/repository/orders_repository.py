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
