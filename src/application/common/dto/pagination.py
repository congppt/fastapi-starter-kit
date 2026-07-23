from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field
TItem = TypeVar("TItem")


class PageQuery(BaseModel):
    """Shared pagination input for list queries."""

    model_config = ConfigDict(frozen=True, from_attributes=True)

    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


class PageResult(BaseModel, Generic[TItem]):
    """Shared pagination output for list queries."""

    model_config = ConfigDict(frozen=True)

    items: list[TItem]
    total: int