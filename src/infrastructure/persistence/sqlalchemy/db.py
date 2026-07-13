from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .settings import DatabaseSettings


def create_engine(settings: DatabaseSettings) -> AsyncEngine:
    """Build an async SQLAlchemy engine from settings."""
    return create_async_engine(
        settings.url,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
        pool_recycle=settings.pool_recycle,
        pool_pre_ping=settings.pool_pre_ping,
        echo=settings.echo,
    )


def create_session_maker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """Create a session factory bound to ``engine``."""
    return async_sessionmaker(bind=engine, expire_on_commit=False)


async def close_db(engine: AsyncEngine) -> None:
    """Dispose the engine and release pooled connections."""
    await engine.dispose()
