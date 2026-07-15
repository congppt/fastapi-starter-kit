from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from mediatr import Mediator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.common.context import ApplicationContext
from application.common.interfaces import ILogger
from application.mediator import create_mediator
from infrastructure.persistence.sqlalchemy.unit_of_work import SqlAlchemyUnitOfWork


def _get_session_maker(request: Request) -> async_sessionmaker[AsyncSession]:
    return request.app.state.session_maker


def _get_logger(request: Request) -> ILogger:
    return request.app.state.logger


async def _get_application_context(
    session_maker: Annotated[
        async_sessionmaker[AsyncSession],
        Depends(_get_session_maker),
    ],
    logger: Annotated[ILogger, Depends(_get_logger)],
) -> AsyncIterator[ApplicationContext]:
    async with SqlAlchemyUnitOfWork(session_maker) as uow:
        yield ApplicationContext(uow=uow, logger=logger)


def get_mediator(
    context: Annotated[ApplicationContext, Depends(_get_application_context)],
) -> Mediator:
    return create_mediator(context)


MediatorDep = Annotated[
    Mediator,
    Depends(get_mediator),
]
