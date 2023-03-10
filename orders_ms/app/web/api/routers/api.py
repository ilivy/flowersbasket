from fastapi import APIRouter

from app.web.api.routers import orders


router = APIRouter()
router.include_router(orders.router)
