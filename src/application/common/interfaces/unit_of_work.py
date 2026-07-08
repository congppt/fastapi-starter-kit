from __future__ import annotations

from types import TracebackType
from typing import Protocol, Self

from .user_repository import IUserRepository


class IUnitOfWork(Protocol):
    """
    Transaction boundary for a single request/use case.

    All repositories exposed here share the same database session.

    Lifecycle contract:
    - Presentation/infrastructure opens the scope.
    - Application handlers assume the unit of work is already open.
    - Handlers call ``commit()`` explicitly after successful writes.
    - On exception, infrastructure rolls back and closes the session.
    """

    users: IUserRepository

    async def __aenter__(self) -> Self:
        """Begin a unit of work (typically opens a DB session)."""

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Roll back on exception and clean up. Does not auto-commit."""

    async def commit(self) -> None:
        """Persist changes made in the current transaction."""

    async def rollback(self) -> None:
        """Roll back the current transaction."""
