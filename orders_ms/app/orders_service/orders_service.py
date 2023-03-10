from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.repository.models import Order
from app.repository.orders_repository import OrdersRepository
from app.web.api.schemas import OrderItemSchema


class OrdersService:
    def __init__(self, db: Session):
        self.orders_repository = OrdersRepository(db)

    def place_order(self, items: List[OrderItemSchema], user_id: UUID) -> Order:
        return self.orders_repository.add(items, user_id)
