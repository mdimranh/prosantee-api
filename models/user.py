from typing import Optional
from sqlmodel import Field
from pydantic import EmailStr
from .fields import PhoneStr
from db.base import TimeStampModel

class UserBase(TimeStampModel):
    email: EmailStr = Field(unique=True, index=True)
    phone: Optional[PhoneStr] = Field(
        nullable=True
    )
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
    phone: Optional[str] = None
    is_active: Optional[bool] = None

class UserRead(UserBase):
    id: int
