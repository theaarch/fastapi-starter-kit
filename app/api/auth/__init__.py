from fastapi import APIRouter

from app.api.auth.login import router as login_router
from app.api.auth.logout import router as logout_router
from app.api.auth.password import router as password_router
from app.api.auth.profile import router as profile_router
from app.api.auth.register import router as register_router

auth_router = APIRouter(prefix="/auth", tags=["auth"])
auth_router.include_router(login_router)
auth_router.include_router(register_router)
auth_router.include_router(logout_router)
auth_router.include_router(profile_router)
auth_router.include_router(password_router)

__all__ = ["auth_router"]
