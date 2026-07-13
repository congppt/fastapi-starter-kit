from __future__ import annotations

from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.common.interfaces import IUserRepository

from .repositories.user_repository import UserRepository


class SqlAlchemyUnitOfWork:
    """SQLAlchemy-backed unit of work sharing one session across repositories."""

    users: IUserRepository

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        self._session = self._session_maker()
        await self._session.__aenter__()
        self.users = UserRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if self._session is None:
            return

        try:
            if exc_type is not None:
                await self.rollback()
        finally:
            await self._session.__aexit__(exc_type, exc_val, exc_tb)
            self._session = None

    async def commit(self) -> None:
        if self._session is None:
            raise RuntimeError("Unit of work is not active")
        await self._session.commit()

    async def rollback(self) -> None:
        if self._session is None:
            raise RuntimeError("Unit of work is not active")
        await self._session.rollback()
