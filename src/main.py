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
