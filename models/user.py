from typing import Optional
from sqlmodel import Field
from pydantic import EmailStr
from db.base import TimeStampModel

class UserBase(TimeStampModel):
    email: EmailStr = Field(unique=True, index=True)
    phone: Optional[str] = Field(
        regex=r"^(01[3-9]\d{8})$",
        description="Bangladesh phone number in format: 01xxxxxxxxx (prefix +88 will be added automatically)",
        nullable=True
    )
    is_active: bool = Field(default=True, nullable=False)
    is_admin: bool = Field(default=False, nullable=False)

    @property
    def formatted_phone(self) -> str:
        return f"+88{self.phone}"

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
