from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Query, status

from application.users.commands.create import CreateUserCommand
from application.users.queries.list import ListUsersQuery
from presentation.api.dependencies import MediatorDep
from presentation.api.schemas import (
    CreateUserRequest,
    CreateUserResponse,
    PageParams,
    PageResponse,
    UserSummaryResponse,
)

router = APIRouter()


@router.post(
    "",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    body: CreateUserRequest,
    mediator: MediatorDep,
) -> CreateUserResponse:
    user_id = await mediator.send_async(
        CreateUserCommand(
            email=body.email,
            name=body.name,
            password=body.password,
        )
    )
    return CreateUserResponse(id=user_id)


@router.get(
    "",
    response_model=PageResponse[UserSummaryResponse],
)
async def list_users(
    mediator: MediatorDep,
    page: Annotated[PageParams, Query()],
) -> PageResponse[UserSummaryResponse]:
    result = await mediator.send_async(
        ListUsersQuery.model_validate(page)
    )
    return PageResponse[UserSummaryResponse](
        items=[UserSummaryResponse.model_validate(item) for item in result.items],
        total=result.total,
        offset=page.offset,
        limit=page.limit,
    )
