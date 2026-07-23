from __future__ import annotations

from typing import Protocol

from domain.entities import User
from domain.valueobjects import Email

from .repository import IRepository


class IUserRepository(IRepository[User, int], Protocol):
    async def get_by_email(self, email: Email) -> User | None: ...

    async def email_exists(self, email: Email) -> bool: ...

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[User], int]:
        """Return a page of users and the total count."""
