from typing import List
from uuid import UUID
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response

from app.orders_service.exceptions import (
    OrderNotFoundError,
    InvalidActionError,
    APIIntegrationError,
)
from app.orders_service.orders_service import OrdersService
from app.web.api.schemas import OrderInSchema, OrderOutSchema, UserSchema
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
    order_details: OrderInSchema,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
) -> OrderOutSchema:
    orders_service = OrdersService(db)
    order = orders_service.place_order(
        **order_details.dict(), user_id=current_user["id"]
    )
    return order


@router.get("/{order_id}", response_model=OrderOutSchema)
async def get_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
) -> OrderOutSchema:
    orders_service = OrdersService(db)
    try:
        order = orders_service.get_order(order_id, user_id=current_user["id"])
    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    return order


@router.get("/", response_model=List[OrderOutSchema])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
) -> List[OrderOutSchema]:
    orders_service = OrdersService(db)
    orders = orders_service.get_orders_list(skip, limit, user_id=current_user["id"])
    return orders


@router.put("/{order_id}", response_model=OrderOutSchema)
async def update_order(
    order_id: UUID,
    order_details: OrderInSchema,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    order_service = OrdersService(db)
    try:
        order = order_service.update_order(
            order_id, **order_details.dict(), user_id=current_user["id"]
        )
    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    return order


@router.delete(
    "/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    order_service = OrdersService(db)
    try:
        order_service.delete_order(order_id, user_id=current_user["id"])
    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{order_id}/cancel", response_model=OrderOutSchema)
async def cancel_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    order_service = OrdersService(db)
    try:
        order = order_service.cancel_order(order_id, user_id=current_user["id"])
    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except InvalidActionError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    return order


@router.post("/{order_id}/pay", response_model=OrderOutSchema)
async def pay_order(
    order_id: UUID,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user),
):
    order_service = OrdersService(db)
    try:
        order = order_service.pay_order(order_id, user_id=current_user["id"])
    except OrderNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except InvalidActionError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except APIIntegrationError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    return order
