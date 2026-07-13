from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities import User
from domain.valueobjects import Email

from ..models import UserModel
from .base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[User, UserModel, int]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, UserModel)

    async def get_by_email(self, email: Email) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == str(email)).limit(1)
        )
        model = result.scalar_one_or_none()
        return model.to_domain_model() if model is not None else None

    async def email_exists(self, email: Email) -> bool:
        result = await self._session.execute(
            select(UserModel.id).where(UserModel.email == str(email)).limit(1)
        )
        return result.scalar_one_or_none() is not None
