from datetime import datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Extra, conint, conlist, validator


class SizeEnum(str, Enum):
    small = "small"
    medium = "medium"
    big = "big"


class StatusEnum(str, Enum):
    created = "created"
    paid = "paid"
    progress = "progress"
    cancelled = "cancelled"
    dispatched = "dispatched"
    delivered = "delivered"


class OrderItemSchema(BaseModel):
    product: str
    size: SizeEnum
    quantity: Optional[conint(ge=1, strict=True)] = 1

    class Config:
        extra = Extra.forbid
        orm_mode = True

    @validator("quantity")
    def quantity_non_nullable(cls, value):
        assert value is not None, "quantity may not be None"
        return value


class OrderBaseSchema(BaseModel):
    items: conlist(OrderItemSchema, min_items=1)


class OrderInSchema(OrderBaseSchema):
    pass


class OrderOutSchema(OrderBaseSchema):
    id: UUID
    created_at: datetime
    status: StatusEnum

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    id: UUID
    username: str
    email: str
