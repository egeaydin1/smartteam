# SmartTeam — Project Management API

A RESTful backend for team-based project management, built with **FastAPI**, **SQLAlchemy 2 (async)**, **PostgreSQL**, and **JWT authentication**.

> Designed by **Ege Aydın & Caner Çakır** — Software Design Patterns course project.

---

## Table of Contents

- [Architecture](#architecture)
- [OOP Principles](#oop-principles)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)

---

## Architecture

```
Client (React + Axios)
        │  HTTP/REST + JWT
        ▼
FastAPI Application
   ├── Routers        (HTTP boundary)
   ├── Services       (business logic)
   ├── Models         (SQLAlchemy ORM)
   └── Schemas        (Pydantic I/O validation)
        │  asyncpg
        ▼
PostgreSQL
```

**Component layers** (from `uml_diagrams_smartteam.pdf`):

| Layer    | Technologies                              |
|----------|-------------------------------------------|
| Client   | React, Axios                              |
| Backend  | FastAPI, JWT Middleware, Pydantic, bcrypt |
| Data     | PostgreSQL, SQLAlchemy ORM                |

---

## OOP Principles

### Encapsulation
- `User.password_hash` is a Python property — raw hash is never exposed; only `verify_password()` / `hash_password()` touch it.
- `User.can_manage_project()` / `can_manage_task()` centralise permission logic inside the model.
- `Task.is_overdue()` / `advance_status()` own their own domain rules.

### Inheritance
- `TimestampMixin` injects `created_at` / `updated_at` into every model without repetition.
- `BaseService[T]` provides generic async CRUD, and concrete services (`UserService`, `ProjectService`, …) inherit it.

### Polymorphism
- `BaseService._base_select()` is overridden by `ProjectService` (eager-loads tasks) and `TaskService` (eager-loads comments) — same interface, specialised behaviour.
- `UserRole` / `TaskStatus` / `TaskPriority` enums enable runtime dispatch in model helpers.

---

## Quick Start

### With Docker

```bash
cp .env.example .env          # fill in SECRET_KEY
docker compose up --build
```

API available at `http://localhost:8000` · Swagger UI at `http://localhost:8000/docs`

### Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env          # configure DATABASE_URL + SECRET_KEY
uvicorn app.main:app --reload
```

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/auth/register` | Register a new user |
| `POST` | `/api/v1/auth/login` | Obtain JWT token |
| `GET`  | `/api/v1/users/me` | Current user profile |
| `GET`  | `/api/v1/projects/` | List projects |
| `POST` | `/api/v1/projects/` | Create a project |
| `PATCH`| `/api/v1/projects/{id}` | Update a project |
| `DELETE`| `/api/v1/projects/{id}` | Delete a project |
| `GET`  | `/api/v1/projects/{id}/tasks/` | List tasks |
| `POST` | `/api/v1/projects/{id}/tasks/` | Create a task |
| `PATCH`| `/api/v1/projects/{id}/tasks/{tid}` | Update a task |
| `POST` | `/api/v1/projects/{id}/tasks/{tid}/advance` | Advance task status |
| `POST` | `/api/v1/projects/{id}/tasks/{tid}/comments/` | Add a comment |

Full interactive docs: `http://localhost:8000/docs`

---

## Running Tests

```bash
pytest --tb=short -q
```

Tests use an **in-memory SQLite** database — no PostgreSQL required for the test suite.

---

## Project Structure

```
smartteam/
├── app/
│   ├── main.py            # FastAPI app & lifespan
│   ├── config.py          # Pydantic settings
│   ├── database.py        # Async engine & session
│   ├── models/            # SQLAlchemy ORM models
│   │   ├── base.py        # DeclarativeBase + enums + TimestampMixin
│   │   ├── user.py
│   │   ├── project.py
│   │   ├── task.py
│   │   └── comment.py
│   ├── schemas/           # Pydantic request/response models
│   ├── services/          # Business logic layer
│   │   ├── base_service.py   # Abstract generic CRUD
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── project_service.py
│   │   ├── task_service.py
│   │   └── comment_service.py
│   ├── routers/           # HTTP endpoints
│   └── core/              # JWT security + DI dependencies
├── tests/
├── .github/workflows/ci.yml
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
└── requirements.txt
```
