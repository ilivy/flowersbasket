from fastapi import APIRouter

from app.web.api.routes import auth, users


router = APIRouter()
router.include_router(auth.router)
router.include_router(users.router)
