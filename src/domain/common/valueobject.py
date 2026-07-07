from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable


class ValueObject(ABC):
    @abstractmethod
    def equality_components(self) -> Iterable[Any]:
        """Return the ordered components that define value equality."""

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False
        if type(other) is not type(self):
            return False
        return tuple(self.equality_components()) == tuple(
            getattr(other, "equality_components")()
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        h = 0
        for component in self.equality_components():
            h = (h * 31) ^ hash(component)
        return h
