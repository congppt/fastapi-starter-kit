from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from infrastructure.persistence.sqlalchemy.db import (
    close_db,
    create_engine,
    create_session_maker,
)
from infrastructure.persistence.sqlalchemy.settings import DatabaseSettings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = DatabaseSettings()
    engine = create_engine(settings)
    app.state.engine = engine
    app.state.session_maker = create_session_maker(engine)
    try:
        yield
    finally:
        await close_db(engine)


app = FastAPI(lifespan=lifespan)
