from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from sqlmodel import select
from models.user import User, UserCreate, UserUpdate
from db.base import CRUDBase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self):
        super().__init__(User)

    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=self.get_password_hash(obj_in.password),
            is_active=True
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def is_active(self, user: User) -> bool:
        return user.is_active

user_service = UserService()