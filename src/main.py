from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.observation.loguru import (
    LoguruSettings,
    configure_logger,
    shutdown_logger,
)
from infrastructure.persistence.sqlalchemy.db import (
    close_db,
    create_engine,
    create_session_maker,
)
from infrastructure.persistence.sqlalchemy.settings import DatabaseSettings
from presentation.api.exception_handler import register_exception_handlers
from presentation.api.v1 import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    app.state.logger = configure_logger(LoguruSettings())
    engine = create_engine(DatabaseSettings())
    app.state.session_maker = create_session_maker(engine)
    try:
        yield
    finally:
        await close_db(engine)
        await shutdown_logger()


app = FastAPI(lifespan=lifespan)
register_exception_handlers(app)
app.include_router(api_router, prefix="/api/v1")
