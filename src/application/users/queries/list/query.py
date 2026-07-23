from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from application.common.dto import PageQuery


class ListUsersQuery(PageQuery):
    """Input for the ListUsers use case."""


class UserSummary(BaseModel):
    """Summary user projection for list queries."""

    model_config = ConfigDict(frozen=True, from_attributes=True)

    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime

    @field_validator("email", mode="before")
    @classmethod
    def coerce_email(cls, value: object) -> object:
        return str(value)
