from fastapi import APIRouter, HTTPException, status

from app.core.dependencies import CurrentUser, DBSession
from app.schemas.comment import CommentCreate, CommentRead, CommentUpdate
from app.services.comment_service import CommentService
from app.services.task_service import TaskService

router = APIRouter(
    prefix="/projects/{project_id}/tasks/{task_id}/comments", tags=["Comments"]
)


async def _get_task_or_404(project_id: int, task_id: int, db):
    task = await TaskService(db).get_by_id(task_id)
    if task is None or task.project_id != project_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found.")
    return task


@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
async def create_comment(
    project_id: int,
    task_id: int,
    payload: CommentCreate,
    current_user: CurrentUser,
    db: DBSession,
) -> CommentRead:
    await _get_task_or_404(project_id, task_id, db)
    return await CommentService(db).create_comment(payload, task_id, current_user)


@router.get("/", response_model=list[CommentRead])
async def list_comments(
    project_id: int, task_id: int, _: CurrentUser, db: DBSession
) -> list[CommentRead]:
    await _get_task_or_404(project_id, task_id, db)
    return await CommentService(db).get_by_task(task_id)


@router.patch("/{comment_id}", response_model=CommentRead)
async def update_comment(
    project_id: int,
    task_id: int,
    comment_id: int,
    payload: CommentUpdate,
    current_user: CurrentUser,
    db: DBSession,
) -> CommentRead:
    await _get_task_or_404(project_id, task_id, db)
    service = CommentService(db)
    comment = await service.get_by_id(comment_id)
    if comment is None or comment.task_id != task_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Comment not found.")
    try:
        return await service.update_comment(comment, payload, current_user)
    except PermissionError as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    project_id: int,
    task_id: int,
    comment_id: int,
    current_user: CurrentUser,
    db: DBSession,
) -> None:
    await _get_task_or_404(project_id, task_id, db)
    service = CommentService(db)
    comment = await service.get_by_id(comment_id)
    if comment is None or comment.task_id != task_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Comment not found.")
    try:
        await service.delete_comment(comment, current_user)
    except PermissionError as exc:
        raise HTTPException(status.HTTP_403_FORBIDDEN, str(exc)) from exc
