from fastapi import APIRouter
from .user.route import router as user_router

api_router = APIRouter()

# Include all endpoint routers here
api_router.include_router(user_router, prefix="/users", tags=["users"])