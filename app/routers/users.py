from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentAdmin, CurrentUser, DBSession
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUser) -> UserRead:
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_me(
    payload: UserUpdate, current_user: CurrentUser, db: DBSession
) -> UserRead:
    return await UserService(db).update_user(current_user, payload)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, _: CurrentUser, db: DBSession) -> UserRead:
    user = await UserService(db).get_by_id(user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found.")
    return user


@router.get("/", response_model=list[UserRead])
async def list_users(
    _: CurrentAdmin,
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
) -> list[UserRead]:
    return await UserService(db).get_all(skip=skip, limit=limit)
