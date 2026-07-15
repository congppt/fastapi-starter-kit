from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel = Literal[
    "TRACE",
    "DEBUG",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
]


class LoguruSettings(BaseSettings):
    """Loguru settings from environment / ``.env``."""

    model_config = SettingsConfigDict(
        env_prefix="LOGURU_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    directory: str = "logs"
    retention_days: int = Field(default=7, ge=1)
    level: LogLevel = "INFO"

    @field_validator("level", mode="before")
    @classmethod
    def normalize_level(cls, value: object) -> object:
        if isinstance(value, str):
            return value.upper()
        return value
