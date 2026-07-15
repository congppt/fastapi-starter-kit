from __future__ import annotations

from fastapi import APIRouter, status

from application.users.commands.create import CreateUserCommand
from presentation.api.dependencies import MediatorDep
from presentation.api.schemas import CreateUserRequest, CreateUserResponse

router = APIRouter(prefix="/users", tags=["users"])


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
