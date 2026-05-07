from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.services.base_service import BaseService


class UserService(BaseService[User]):
    """Encapsulates all user-related business logic."""

    def __init__(self, db: AsyncSession) -> None:
        super().__init__(db)

    @property
    def _model(self) -> type[User]:
        return User

    async def get_by_email(self, email: str) -> User | None:
        result = await self._db.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        result = await self._db.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def register(self, data: UserCreate) -> User:
        user = User(
            username=data.username,
            email=data.email,
            role=data.role,
        )
        user.password_hash = hash_password(data.password)
        return await self.create(user)

    async def authenticate(self, email: str, password: str) -> User | None:
        user = await self.get_by_email(email)
        if user is None or not verify_password(password, user.password_hash):
            return None
        return user

    async def update_user(self, user: User, data: UserUpdate) -> User:
        return await self.update(user, data.model_dump(exclude_none=True))
