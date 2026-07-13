from __future__ import annotations

from mediatr import Mediator

from application.common.exceptions import ValidationException
from application.common.interfaces import IHasher, IUnitOfWork
from domain.entities import User
from domain.valueobjects import Email

from .command import CreateUserCommand


@Mediator.handler
class CreateUserHandler:
    def __init__(self, uow: IUnitOfWork, hasher: IHasher) -> None:
        self._uow = uow
        self._hasher = hasher

    async def handle(self, command: CreateUserCommand) -> int:
        email = Email(command.email)

        if await self._uow.users.email_exists(email):
            raise ValidationException(
                "Email is already registered.",
                code="EMAIL_TAKEN",
            )

        user = User(
            email=email,
            name=command.name,
            password_hash=self._hasher.hash(command.password),
        )

        created = await self._uow.users.add(user)

        await self._uow.commit()

        return created.id
