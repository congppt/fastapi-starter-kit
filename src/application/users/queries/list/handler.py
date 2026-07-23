from __future__ import annotations

from mediatr import Mediator

from application.common.dto import PageResult
from application.common.interfaces import IUnitOfWork

from .query import ListUsersQuery, UserSummary


@Mediator.handler
class ListUsersQueryHandler:
    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow

    async def handle(self, query: ListUsersQuery) -> PageResult[UserSummary]:
        users, total = await self._uow.users.list(
            offset=query.offset,
            limit=query.limit,
        )
        return PageResult(
            items=[UserSummary.model_validate(user) for user in users],
            total=total,
        )
