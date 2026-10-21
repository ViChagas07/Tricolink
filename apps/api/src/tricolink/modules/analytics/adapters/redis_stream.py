from __future__ import annotations

import asyncio
from typing import Any, cast

from redis.asyncio import Redis
from redis.exceptions import RedisError

from tricolink.core.config import Settings
from tricolink.infra.observability.metrics import record_click_dropped
from tricolink.infra.resilience import CircuitBreaker, CircuitOpenError
from tricolink.modules.analytics.domain.click import ClickEvent


class RedisClickPublisher:
    def __init__(
        self,
        redis: Redis,
        *,
        breaker: CircuitBreaker | None,
        settings: Settings,
    ) -> None:
        self._redis = redis
        self._breaker = breaker
        self._stream_key = settings.click_stream_key
        self._maxlen = settings.click_stream_maxlen
        self._timeout = settings.click_publish_timeout_seconds

    async def publish(self, event: ClickEvent) -> bool:
        fields = {
            "link_id": str(event.link_id),
            "clicked_at": event.clicked_at.isoformat(),
            "country": event.country or "",
            "device": event.device,
            "browser": event.browser or "",
            "referrer_host": event.referrer_host or "",
        }

        async def operation() -> None:
            await asyncio.wait_for(
                self._redis.xadd(
                    self._stream_key,
                    cast(Any, fields),
                    maxlen=self._maxlen,
                    approximate=True,
                ),
                timeout=self._timeout,
            )

        try:
            if self._breaker is None:
                await operation()
            else:
                async with self._breaker.guard():
                    await operation()
        except (RedisError, TimeoutError, OSError, CircuitOpenError):
            record_click_dropped("redis_unavailable")
            return False
        return True
