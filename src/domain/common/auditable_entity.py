import datetime
from typing import TypeVar

from .entity import BaseEntity

TId = TypeVar("TId")


class BaseAuditableEntity(BaseEntity[TId]):
    created_at: datetime | None
    created_by: str | None
    updated_at: datetime | None
    updated_by: str | None

    def __init__(
        self,
        *,
        id: TId | None = None,
        created_at: datetime | None = None,
        created_by: str | None = None,
        updated_at: datetime | None = None,
        updated_by: str | None = None,
    ) -> None:
        super().__init__(id=id)
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
