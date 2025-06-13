from typing import Optional
from sqlmodel import Field
from pydantic import EmailStr
from db.base import TimeStampModel

class UserBase(TimeStampModel):
    email: EmailStr = Field(unique=True, index=True)
    username: str = Field(max_length=50, unique=True, index=True)
    is_active: bool = Field(default=True, nullable=False)
    is_admin: bool = Field(default=False, nullable=False)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None

class UserRead(UserBase):
    id: int
