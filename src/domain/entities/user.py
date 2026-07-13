from __future__ import annotations

from datetime import datetime

from domain.common import BaseAuditableEntity
from domain.exceptions import InvalidEntityStateException
from domain.valueobjects import Email


class User(BaseAuditableEntity[int]):
    email: Email
    name: str
    password_hash: str
    is_active: bool

    def __init__(
        self,
        *,
        id: int | None = None,
        email: Email,
        name: str,
        password_hash: str,
        is_active: bool = True,
        created_at: datetime | None = None,
        created_by: str | None = None,
        updated_at: datetime | None = None,
        updated_by: str | None = None,
    ) -> None:
        super().__init__(
            id=id,
            created_at=created_at,
            created_by=created_by,
            updated_at=updated_at,
            updated_by=updated_by,
        )

        self.email = email
        self.name = name.strip()
        self.password_hash = password_hash
        self.is_active = is_active

        self._validate()

    def _validate(self):
        if not self.name:
            raise InvalidEntityStateException("User name cannot be empty")
        if not self.password_hash:
            raise InvalidEntityStateException("Password hash cannot be empty")

    def change_name(self, new_name: str):
        new_name = new_name.strip()
        if not new_name:
            raise InvalidEntityStateException("User name cannot be empty")
        self.name = new_name

    def change_email(self, new_email: Email):
        self.email = new_email

    def set_password_hash(self, password_hash: str):
        if not password_hash:
            raise InvalidEntityStateException("Password hash cannot be empty")
        self.password_hash = password_hash

    def deactivate(self):
        self.is_active = False

    def activate(self):
        self.is_active = True
