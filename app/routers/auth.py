from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import DBSession
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: DBSession) -> UserRead:
    service = UserService(db)
    if await service.get_by_email(payload.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered.")
    if await service.get_by_username(payload.username):
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken.")
    return await service.register(payload)


@router.post("/login", response_model=Token)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: DBSession,
) -> Token:
    try:
        # OAuth2PasswordRequestForm uses `username` field; we treat it as email
        return await AuthService(db).login(form.username, form.password)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
