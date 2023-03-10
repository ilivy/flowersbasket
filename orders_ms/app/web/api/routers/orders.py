from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, status

from app.orders_service.orders_service import OrdersService
from app.web.api.schemas import OrderInSchema, OrderOutSchema
from app.web.dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderOutSchema,
)
async def create_order(
    payload: OrderInSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    orders_service = OrdersService(db)
    order = orders_service.place_order(**payload.dict(), user_id=current_user["id"])
    return order
