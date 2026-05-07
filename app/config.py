import json
from functools import lru_cache
from typing import Any

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "SmartTeam"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    DATABASE_URL: PostgresDsn = "postgresql+asyncpg://postgres:postgres@localhost:5432/smartteam"  # type: ignore[assignment]

    SECRET_KEY: str = "change-me-in-production-use-a-long-random-string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Accepts a JSON array string from the environment:
    # ALLOWED_ORIGINS='["http://localhost:5173","http://localhost:3000"]'
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://frontend:5173",
    ]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("SECRET_KEY")
    @classmethod
    def secret_key_min_length(cls, v: str) -> str:
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long.")
        return v

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # comma-separated fallback: "url1,url2"
                return [s.strip() for s in v.split(",") if s.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()
