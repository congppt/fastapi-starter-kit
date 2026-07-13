from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Postgres / SQLAlchemy settings from environment / ``.env``."""

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    url: str
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 2
    pool_timeout: int = 30
    pool_recycle: int = 1800
    pool_pre_ping: bool = True
