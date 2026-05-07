from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.models.user import User
from app.schemas.token import Token
from app.services.user_service import UserService


class AuthService:
    """Handles login and token issuance."""

    def __init__(self, db: AsyncSession) -> None:
        self._user_service = UserService(db)

    async def login(self, email: str, password: str) -> Token:
        user = await self._user_service.authenticate(email, password)
        if user is None:
            raise ValueError("Invalid email or password.")
        return self._issue_token(user)

    @staticmethod
    def _issue_token(user: User) -> Token:
        access_token = create_access_token(
            {"sub": str(user.id), "username": user.username}
        )
        return Token(access_token=access_token)
