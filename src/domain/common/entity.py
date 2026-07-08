from __future__ import annotations

from typing import Generic, TypeVar

from .event import BaseEvent

TId = TypeVar("TId")


class BaseEntity(Generic[TId]):
    id: TId

    def __init__(self, *, id: TId | None = None) -> None:
        if id is not None:
            self.id = id
        self._domain_events: list[BaseEvent] = []

    @property
    def domain_events(self):
        return tuple(self._domain_events)

    def add_domain_event(self, event: BaseEvent):
        self._domain_events.append(event)

    def remove_domain_event(self, event: BaseEvent):
        self._domain_events.remove(event)

    def clear_domain_events(self):
        self._domain_events.clear()
