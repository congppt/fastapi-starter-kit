from __future__ import annotations

from dataclasses import dataclass

from ..exceptions import InvalidEntityStateException
from ..common.valueobject import ValueObject


@dataclass(frozen=True, eq=False)
class Email(ValueObject):
    value: str

    def __post_init__(self) -> None:
        normalized = self.value.strip().lower()
        if not normalized:
            raise InvalidEntityStateException("Email is required")

        if "@" not in normalized:
            raise InvalidEntityStateException("Email must contain '@'")

        object.__setattr__(self, "value", normalized)

    def equality_components(self):
        yield self.value

    def __str__(self) -> str:
        return self.value
