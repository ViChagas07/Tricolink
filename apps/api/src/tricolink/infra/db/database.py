from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from tricolink.core.config import Settings
from tricolink.infra.db.engine import create_engine, create_session_factory
from tricolink.infra.db.unit_of_work import unit_of_work
from tricolink.infra.resilience import Bulkhead, CircuitBreaker


class Database:
    """Async engine owner with health checks and unit-of-work helpers."""

    def __init__(
        self,
        settings: Settings,
        *,
        breaker: CircuitBreaker | None = None,
        read_bulkhead: Bulkhead | None = None,
        write_bulkhead: Bulkhead | None = None,
    ) -> None:
        self._settings = settings
        self._engine = create_engine(settings)
        self._session_factory = create_session_factory(self._engine)
        self._breaker = breaker
        self._read_bulkhead = read_bulkhead
        self._write_bulkhead = write_bulkhead

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        return self._session_factory

    async def ping(self) -> None:
        async with AsyncExitStack() as stack:
            if self._read_bulkhead is not None:
                await stack.enter_async_context(self._read_bulkhead.acquire())
            if self._breaker is not None:
                await stack.enter_async_context(self._breaker.guard())
            async with asyncio.timeout(self._settings.db_connect_timeout_seconds):
                async with self._engine.connect() as connection:
                    await connection.execute(text("SELECT 1"))

    async def check_ready(self) -> None:
        async with AsyncExitStack() as stack:
            if self._read_bulkhead is not None:
                await stack.enter_async_context(self._read_bulkhead.acquire())
            if self._breaker is not None:
                await stack.enter_async_context(self._breaker.guard())
            async with asyncio.timeout(self._settings.db_connect_timeout_seconds):
                async with self._engine.connect() as connection:
                    migrated = await connection.scalar(
                        text(
                            "SELECT "
                            "to_regclass('public.users') IS NOT NULL "
                            "AND to_regclass('public.links') IS NOT NULL "
                            "AND to_regclass('public.refresh_tokens') IS NOT NULL"
                        )
                    )
        if not migrated:
            raise RuntimeError("database schema is not migrated")

    @asynccontextmanager
    async def read(self) -> AsyncIterator[AsyncSession]:
        async with AsyncExitStack() as stack:
            if self._read_bulkhead is not None:
                await stack.enter_async_context(self._read_bulkhead.acquire())
            if self._breaker is not None:
                await stack.enter_async_context(self._breaker.guard())
            session = self._session_factory()
            try:
                yield session
            finally:
                await session.close()

    @asynccontextmanager
    async def unit_of_work(self) -> AsyncIterator[AsyncSession]:
        async with AsyncExitStack() as stack:
            if self._write_bulkhead is not None:
                await stack.enter_async_context(self._write_bulkhead.acquire())
            if self._breaker is not None:
                await stack.enter_async_context(self._breaker.guard())
            async with unit_of_work(self._session_factory) as session:
                yield session

    async def dispose(self) -> None:
        await self._engine.dispose()
