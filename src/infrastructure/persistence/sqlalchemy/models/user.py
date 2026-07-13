from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from domain.entities import User
from domain.valueobjects import Email

from .base import Base


class UserModel(Base[User]):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    created_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )
    updated_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

    def to_domain_model(self) -> User:
        return User(
            id=self.id,
            email=Email(self.email),
            name=self.name,
            password_hash=self.password_hash,
            is_active=self.is_active,
            created_at=self.created_at,
            created_by=self.created_by,
            updated_at=self.updated_at,
            updated_by=self.updated_by,
        )

    @classmethod
    def from_domain_model(cls, entity: User) -> UserModel:
        model = cls(
            email=str(entity.email),
            name=entity.name,
            password_hash=entity.password_hash,
            is_active=entity.is_active,
            created_by=entity.created_by,
            updated_by=entity.updated_by,
        )
        if getattr(entity, "id", None) is not None:
            model.id = entity.id
        if entity.created_at is not None:
            model.created_at = entity.created_at
        if entity.updated_at is not None:
            model.updated_at = entity.updated_at
        return model
