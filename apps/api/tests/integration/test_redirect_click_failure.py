from __future__ import annotations

import asyncio
from dataclasses import replace
from typing import cast
from uuid import uuid4

import httpx
import pytest
from prometheus_client import REGISTRY
from redis.asyncio import Redis
from redis.exceptions import ConnectionError as RedisConnectionError

from tricolink.core.config import Settings
from tricolink.main import create_app
from tricolink.modules.analytics.adapters import RedisClickPublisher
from tricolink.modules.links.application import RecordClick, ResolvedLink
from tricolink.modules.links.domain.entities import LinkState
from tricolink.modules.links.presentation.dependencies import (
    get_record_click,
    get_resolve_link,
)
from tricolink.shared_kernel.clock import SystemClock

pytestmark = pytest.mark.integration


class StaticResolve:
    async def execute(self, code: str) -> ResolvedLink:
        return ResolvedLink(
            link_id=1,
            original_url="https://93.184.216.34/click",
            state=LinkState.ACTIVE,
        )


class DownRedis:
    async def xadd(self, *args: object, **kwargs: object) -> None:
        raise RedisConnectionError("down")


class BlockingPublisher:
    def __init__(self) -> None:
        self.started = asyncio.Event()
        self.release = asyncio.Event()

    async def publish(self, event: object) -> bool:
        self.started.set()
        await self.release.wait()
        return True


def click_settings() -> Settings:
    return replace(
        Settings.from_env(),
        click_flusher_enabled=False,
        click_stream_key=f"test:clicks-failure:{uuid4().hex[:10]}",
        rl_redirect_capacity=100,
        rl_redirect_refill_per_sec=100,
        rl_global_capacity=10_000,
        rl_global_refill_per_sec=10_000,
    )


@pytest.mark.asyncio
async def test_redirect_does_not_wait_for_click_publisher() -> None:
    settings = click_settings()
    publisher = BlockingPublisher()
    recorder = RecordClick(clock=SystemClock(), publisher=publisher)
    app = create_app(settings)
    app.dependency_overrides[get_resolve_link] = StaticResolve
    app.dependency_overrides[get_record_click] = lambda: recorder

    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/api/v1/r/any-code")

        assert response.status_code == 302
        await asyncio.wait_for(publisher.started.wait(), timeout=1)
        assert publisher.release.is_set() is False

        publisher.release.set()
        await recorder.drain()
    finally:
        publisher.release.set()
        await recorder.drain()
        await app.state.services.close()


@pytest.mark.asyncio
async def test_redirect_continues_and_metric_counts_dropped_click() -> None:
    settings = click_settings()
    publisher = RedisClickPublisher(
        cast(Redis, DownRedis()),
        breaker=None,
        settings=settings,
    )
    recorder = RecordClick(clock=SystemClock(), publisher=publisher)
    app = create_app(settings)
    app.dependency_overrides[get_resolve_link] = StaticResolve
    app.dependency_overrides[get_record_click] = lambda: recorder
    before = (
        REGISTRY.get_sample_value(
            "tricolink_clicks_dropped_total",
            {"reason": "redis_unavailable"},
        )
        or 0
    )

    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app),
            base_url="http://test",
        ) as client:
            response = await client.get("/api/v1/r/any-code")

        assert response.status_code == 302
        await recorder.drain()

        after = (
            REGISTRY.get_sample_value(
                "tricolink_clicks_dropped_total",
                {"reason": "redis_unavailable"},
            )
            or 0
        )
        assert after == before + 1
    finally:
        await recorder.drain()
        await app.state.services.close()
