from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.orders_service.exceptions import (
    OrderNotFoundError,
    InvalidActionError,
    APIIntegrationError,
)
from app.repository.models import Order
from app.repository.orders_repository import OrdersRepository
from app.web.api.schemas import OrderItemSchema


class OrdersService:
    def __init__(self, db: Session):
        self.orders_repository = OrdersRepository(db)

    def place_order(self, items: List[OrderItemSchema], user_id: UUID) -> Order:
        return self.orders_repository.add(items, user_id)

    def get_order(self, order_id: UUID, **filters) -> Order:
        order = self.orders_repository.get(order_id, **filters)
        if order is not None:
            return order
        raise OrderNotFoundError(f"Order with ID {order_id} not found")

    def get_orders_list(self, skip: int = 1, limit: int = 100, **filters) -> List:
        orders = self.orders_repository.list(skip, limit, **filters)
        return orders

    def update_order(self, order_id: UUID, items: List[OrderItemSchema], user_id: UUID):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        return self.orders_repository.update(order_id, items=items)

    def delete_order(self, order_id: UUID, user_id: UUID):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        return self.orders_repository.delete(order_id)

    def cancel_order(self, order_id: UUID, user_id: UUID):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
        if order.status in ["dispatched", "delivered"]:
            raise InvalidActionError(f"Cannot cancel order with ID {order_id}")
        return self.orders_repository.update(order_id, status="cancelled")

    def pay_order(self, order_id: UUID, user_id: UUID):
        order = self.orders_repository.get(order_id, user_id=user_id)
        if order is None:
            raise OrderNotFoundError(f"Order with ID {order_id} not found")
        if order.status != "created":
            raise InvalidActionError(f"Order with ID {order_id} has already been paid")

        # TODO: Integrate Payments
        # response = requests.post(
        #     'http://localhost:3001/payments', json={'order_id': self.id}
        # )
        # if response.status_code == 201:
        #     return
        raise APIIntegrationError(
            f"Could not process payment for Order with ID {order_id}"
        )

        # TODO: Integrate Scheduling
        # response = requests.post(
        #     'http://localhost:3000/studio/schedules',
        #     json={'order': [item.dict() for item in self.items]}
        # )
        # if response.status_code == 201:
        #     schedule_id = response.json()['id']
        raise APIIntegrationError(f"Could not schedule Order with ID {order_id}")

        return self.orders_repository.update(
            order_id, status="paid", schedule_id=schedule_id
        )
