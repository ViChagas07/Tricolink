from __future__ import annotations

import asyncio

from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

from tricolink.core.config import Settings


def create_redis(settings: Settings) -> Redis:
    pool = ConnectionPool.from_url(
        settings.redis_url,
        max_connections=settings.redis_pool_max_connections,
        socket_timeout=settings.redis_timeout_seconds,
        socket_connect_timeout=settings.redis_connect_timeout_seconds,
        health_check_interval=30,
        decode_responses=True,
    )
    return Redis(connection_pool=pool)


async def ping_redis(redis: Redis, *, timeout_seconds: float = 2.0) -> None:
    await asyncio.wait_for(redis.ping(), timeout=timeout_seconds)


async def close_redis(redis: Redis) -> None:
    await redis.aclose()
