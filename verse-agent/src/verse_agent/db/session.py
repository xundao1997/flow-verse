"""Async SQLAlchemy engine and session management."""

from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from verse_agent.core.config import DatabaseSettings


class DatabaseManager:
    """Create and manage SQLAlchemy async engine and sessions."""

    def __init__(self, settings: DatabaseSettings) -> None:
        self._settings = settings
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    def _configure(self) -> None:
        if self._engine is not None and self._session_factory is not None:
            return

        self._engine = create_async_engine(
            self._settings.sqlalchemy_url,
            echo=self._settings.echo,
            pool_pre_ping=self._settings.pool_pre_ping,
            pool_recycle=self._settings.pool_recycle,
            pool_size=self._settings.pool_size,
            max_overflow=self._settings.max_overflow,
            connect_args={"connect_timeout": self._settings.connect_timeout},
        )
        self._session_factory = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            autoflush=False,
        )

    @property
    def engine(self) -> AsyncEngine:
        """Return the lazily created async engine."""
        self._configure()
        assert self._engine is not None
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Return the lazily created async session factory."""
        self._configure()
        assert self._session_factory is not None
        return self._session_factory

    async def get_session(self) -> AsyncIterator[AsyncSession]:
        """Yield an async database session."""
        async with self.session_factory() as session:
            yield session

    async def ping(self) -> bool:
        """Probe database availability with a lightweight query."""
        async with self.engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return True

    async def dispose(self) -> None:
        """Dispose the current engine."""
        if self._engine is not None:
            await self._engine.dispose()
            self._engine = None
            self._session_factory = None
