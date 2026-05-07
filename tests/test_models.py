"""Unit tests for domain logic on model instances (no DB needed)."""

from datetime import date, timedelta

import pytest

from app.models.base import TaskPriority, TaskStatus, UserRole
from app.models.project import Project
from app.models.task import Task
from app.models.user import User


def make_user(role: UserRole = UserRole.MEMBER, user_id: int = 1) -> User:
    u = User(id=user_id, username="u", email="u@x.com", role=role)
    u.password_hash = "hashed"
    return u


def make_project(owner_id: int = 1) -> Project:
    return Project(id=1, title="P", owner_id=owner_id)


def make_task(assigned_to: int | None = 1) -> Task:
    return Task(
        id=1,
        title="T",
        status=TaskStatus.TO_DO,
        priority=TaskPriority.HIGH,
        project_id=1,
        assigned_to=assigned_to,
    )


class TestUserRoles:
    def test_admin_is_admin(self):
        assert make_user(UserRole.ADMIN).is_admin()

    def test_member_is_not_admin(self):
        assert not make_user(UserRole.MEMBER).is_admin()

    def test_admin_can_manage_any_project(self):
        admin = make_user(UserRole.ADMIN, user_id=99)
        project = make_project(owner_id=1)
        assert admin.can_manage_project(project)

    def test_owner_can_manage_own_project(self):
        user = make_user(user_id=1)
        project = make_project(owner_id=1)
        assert user.can_manage_project(project)

    def test_non_owner_cannot_manage_project(self):
        user = make_user(user_id=2)
        project = make_project(owner_id=1)
        assert not user.can_manage_project(project)


class TestTaskDomain:
    def test_advance_status_to_do_to_in_progress(self):
        task = make_task()
        assert task.advance_status() == TaskStatus.IN_PROGRESS

    def test_advance_status_in_progress_to_done(self):
        task = make_task()
        task.status = TaskStatus.IN_PROGRESS
        assert task.advance_status() == TaskStatus.DONE

    def test_advance_status_done_stays_done(self):
        task = make_task()
        task.status = TaskStatus.DONE
        assert task.advance_status() == TaskStatus.DONE

    def test_is_overdue_past_deadline(self):
        task = make_task()
        task.deadline = date.today() - timedelta(days=1)
        assert task.is_overdue()

    def test_is_not_overdue_future_deadline(self):
        task = make_task()
        task.deadline = date.today() + timedelta(days=1)
        assert not task.is_overdue()

    def test_done_task_never_overdue(self):
        task = make_task()
        task.status = TaskStatus.DONE
        task.deadline = date.today() - timedelta(days=10)
        assert not task.is_overdue()
