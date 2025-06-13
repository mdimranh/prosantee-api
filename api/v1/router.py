from fastapi import APIRouter
from .user.route import router as user_router
from .auth.route import router as auth_router

api_router = APIRouter()

# Include all endpoint routers here
api_router.include_router(user_router, prefix="/users", tags=["users"])
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])