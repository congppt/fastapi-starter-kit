from __future__ import annotations

from typing import Generic, Self, TypeVar

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

TEntity = TypeVar("TEntity")


class Base(DeclarativeBase, Generic[TEntity]):
    """
    Declarative base for ORM models.

    Subclasses must implement domain mapping:
    - ``to_domain_model`` — ORM → domain
    - ``from_domain_model`` — domain → ORM
    """
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


    def to_domain_model(self) -> TEntity:
        raise NotImplementedError(
            f"{type(self).__name__} must implement to_domain_model()"
        )

    @classmethod
    def from_domain_model(cls, entity: TEntity) -> Self:
        raise NotImplementedError(
            f"{cls.__name__} must implement from_domain_model()"
        )
