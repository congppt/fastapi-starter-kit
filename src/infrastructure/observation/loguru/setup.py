from __future__ import annotations

from datetime import timedelta
from pathlib import Path

from loguru import logger
from loguru._logger import Logger

from .settings import LoguruSettings


def configure_logger(settings: LoguruSettings) -> Logger:
    """Configure the process-wide loguru logger (JSON file, daily rotation, enqueue)."""

    logger.remove()

    log_dir = Path(settings.directory)
    log_dir.mkdir(parents=True, exist_ok=True)

    logger.add(
        log_dir / "{time:YY-MM-DD}.log",
        level=settings.level,
        serialize=True,
        enqueue=True,
        encoding="utf-8",
        rotation=timedelta(days=1),
        retention=timedelta(days=settings.retention_days),
    )
    return logger


async def shutdown_logger() -> None:
    """Flush the enqueue worker and detach sinks before process exit."""

    await logger.complete()
    logger.remove()
