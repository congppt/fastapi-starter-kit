from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.common.context import ApplicationContext
from infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork


def _get_session_maker(request: Request) -> async_sessionmaker[AsyncSession]:
    return request.app.state.session_maker


async def get_application_context(
    session_maker: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(_get_session_maker),
    ],
) -> AsyncIterator[ApplicationContext]:
    async with SqlAlchemyUnitOfWork(session_maker) as uow:
        yield ApplicationContext(uow=uow)


ApplicationContextDep = Annotated[
    ApplicationContext,
    Depends(get_application_context),
]
