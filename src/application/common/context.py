from __future__ import annotations

from dataclasses import dataclass

from application.common.interfaces import IUnitOfWork


@dataclass(frozen=True, slots=True)
class ApplicationContext:
    """Bag of shared dependencies between handlers/behaviors"""

    uow: IUnitOfWork
