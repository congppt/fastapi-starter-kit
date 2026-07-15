import time
from collections.abc import Awaitable, Callable
from typing import Any

from application.common.interfaces import ILogger


class LogBehavior:
    """Logs handler entry, exit, and elapsed time for every request."""

    def __init__(self, logger: ILogger) -> None:
        self._logger = logger

    async def handle(
        self,
        request: object,
        next: Callable[[], Awaitable[Any]],
    ) -> Any:
        request_name = type(request).__name__
        self._logger.info(f"Handling {request_name}")
        started = time.perf_counter()
        try:
            result = await next()
        except Exception:
            self._logger.exception(f"Failed to handle {request_name}")
            raise

        elapsed_ms = (time.perf_counter() - started) * 1000
        self._logger.info(f"Handled {request_name} in {elapsed_ms:.2f}ms")
        return result
