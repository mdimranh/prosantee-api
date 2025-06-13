from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from models.user import User, UserCreate, UserUpdate, UserRead
from .service import user_service

router = APIRouter()

@router.get("/", response_model=List[UserRead])
async def read_users(
    db: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
):
    """Retrieve users with pagination."""
    return await user_service.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    db: AsyncSession = Depends(get_session),
    user_in: UserCreate,
):
    """Create new user with proper password hashing."""
    user = await user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists."
        )
    user = await user_service.create(db, obj_in=user_in)
    return user

@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_session),
):
    """Get user by ID."""
    user = await user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    *,
    db: AsyncSession = Depends(get_session),
    user_id: int,
    user_in: UserUpdate,
):
    """Update user information."""
    user = await user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_service.update(db, db_obj=user, obj_in=user_in)

@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(
    *,
    db: AsyncSession = Depends(get_session),
    user_id: int,
):
    """Delete user."""
    user = await user_service.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_service.delete(db, id=user_id)