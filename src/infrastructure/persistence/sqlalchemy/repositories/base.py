from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.base import Base

TEntity = TypeVar("TEntity")
TModel = TypeVar("TModel", bound=Base)
TId = TypeVar("TId")


class SqlAlchemyRepository(Generic[TEntity, TModel, TId]):
    """
    Shared SQLAlchemy CRUD for domain entities.

    Mapping lives on ORM models via ``to_domain_model`` / ``from_domain_model``.
    """

    def __init__(self, session: AsyncSession, model_cls: type[TModel]) -> None:
        self._session = session
        self._model_cls = model_cls

    async def get_by_id(self, entity_id: TId) -> TEntity | None:
        model = await self._session.get(self._model_cls, entity_id)
        return model.to_domain_model() if model is not None else None

    async def add(self, entity: TEntity) -> TEntity:
        model = self._model_cls.from_domain_model(entity)
        self._session.add(model)
        await self._session.flush()
        return model.to_domain_model()

    async def update(self, entity: TEntity) -> TEntity:
        model = self._model_cls.from_domain_model(entity)
        merged = await self._session.merge(model)
        await self._session.flush()
        return merged.to_domain_model()

    async def delete(self, entity_id: TId) -> bool:
        model = await self._session.get(self._model_cls, entity_id)
        if model is None:
            return False
        await self._session.delete(model)
        await self._session.flush()
        return True

    async def exists(self, entity_id: TId) -> bool:
        id_column: Any = getattr(self._model_cls, "id")
        result = await self._session.execute(
            select(id_column).where(id_column == entity_id).limit(1)
        )
        return result.scalar_one_or_none() is not None
