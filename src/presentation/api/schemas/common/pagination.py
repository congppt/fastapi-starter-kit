from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, computed_field

TItem = TypeVar("TItem")


class PageParams(BaseModel):
    """Shared query params for paginated list endpoints."""

    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=20, ge=1, le=100)


class PageResponse(BaseModel, Generic[TItem]):
    """HTTP pagination envelope shared by list endpoints."""

    model_config = ConfigDict(frozen=True)

    items: list[TItem]
    total: int
    offset: int
    limit: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def has_next(self) -> bool:
        return self.offset + self.limit < self.total

    @computed_field  # type: ignore[prop-decorator]
    @property
    def has_prev(self) -> bool:
        return self.offset > 0
