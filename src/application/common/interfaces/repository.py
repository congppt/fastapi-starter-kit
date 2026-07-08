from __future__ import annotations

from typing import Protocol, TypeVar

TEntity = TypeVar("TEntity")
TId = TypeVar("TId")


class IRepository(Protocol[TEntity, TId]):
    """
    Generic repository contract for aggregate/entity persistence.

    Infrastructure implementations are responsible for mapping between
    domain entities and ORM models.
    """

    async def get_by_id(self, entity_id: TId) -> TEntity | None:
        """Load an entity by its identifier."""

    def add(self, entity: TEntity) -> TEntity:
        """Persist a new entity and return it with generated fields (e.g. id)."""

    async def update(self, entity: TEntity) -> TEntity:
        """Persist changes to an existing entity."""

    async def delete(self, entity_id: TId) -> bool:
        """Delete an entity by id. Returns True if deleted, False if not found."""

    async def exists(self, entity_id: TId) -> bool:
        """Return True when an entity with the given id exists."""
