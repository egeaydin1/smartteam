from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate, current_user: CurrentUser, db: DBSession
) -> ProjectRead:
    return await ProjectService(db).create_project(payload, current_user)


@router.get("/", response_model=list[ProjectRead])
async def list_projects(
    current_user: CurrentUser,
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
) -> list[ProjectRead]:
    if current_user.is_admin():
        return await ProjectService(db).get_all(skip=skip, limit=limit)
    return await ProjectService(db).get_by_owner(current_user.id)


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: int, current_user: CurrentUser, db: DBSession
) -> ProjectRead:
    project = await ProjectService(db).get_by_id(project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found.")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    payload: ProjectUpdate,
    current_user: CurrentUser,
    db: DBSession,
) -> ProjectRead:
    service = ProjectService(db)
    project = await service.get_by_id(project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found.")
    try:
        return await service.update_project(project, payload, current_user)
    except PermissionError as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int, current_user: CurrentUser, db: DBSession
) -> None:
    service = ProjectService(db)
    project = await service.get_by_id(project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found.")
    try:
        await service.delete_project(project, current_user)
    except PermissionError as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc
