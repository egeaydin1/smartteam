from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


async def _get_project_or_404(project_id: int, db):
    project = await ProjectService(db).get_by_id(project_id)
    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found.")
    return project


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    project_id: int,
    payload: TaskCreate,
    current_user: CurrentUser,
    db: DBSession,
) -> TaskRead:
    await _get_project_or_404(project_id, db)
    return await TaskService(db).create_task(payload, project_id)


@router.get("/", response_model=list[TaskRead])
async def list_tasks(
    project_id: int, _: CurrentUser, db: DBSession
) -> list[TaskRead]:
    await _get_project_or_404(project_id, db)
    return await TaskService(db).get_by_project(project_id)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    project_id: int, task_id: int, _: CurrentUser, db: DBSession
) -> TaskRead:
    task = await TaskService(db).get_by_id(task_id)
    if task is None or task.project_id != project_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    project_id: int,
    task_id: int,
    payload: TaskUpdate,
    current_user: CurrentUser,
    db: DBSession,
) -> TaskRead:
    service = TaskService(db)
    task = await service.get_by_id(task_id)
    if task is None or task.project_id != project_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    try:
        return await service.update_task(task, payload, current_user)
    except PermissionError as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc


@router.post("/{task_id}/advance", response_model=TaskRead)
async def advance_task(
    project_id: int, task_id: int, current_user: CurrentUser, db: DBSession
) -> TaskRead:
    service = TaskService(db)
    task = await service.get_by_id(task_id)
    if task is None or task.project_id != project_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    try:
        return await service.advance_task_status(task, current_user)
    except PermissionError as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    project_id: int, task_id: int, current_user: CurrentUser, db: DBSession
) -> None:
    service = TaskService(db)
    task = await service.get_by_id(task_id)
    if task is None or task.project_id != project_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    try:
        await service.delete_task(task, current_user)
    except PermissionError as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc
