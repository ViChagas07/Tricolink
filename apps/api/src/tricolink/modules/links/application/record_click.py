from __future__ import annotations

import asyncio
from contextlib import suppress

from tricolink.modules.analytics.domain.click import (
    ClickEvent,
    extract_referrer_host,
    normalize_country,
    parse_user_agent,
)
from tricolink.modules.links.application.ports import ClickPublisher, Clock


class RecordClick:
    """Builds a privacy-safe click event and never blocks the redirect on it."""

    def __init__(self, *, clock: Clock, publisher: ClickPublisher) -> None:
        self._clock = clock
        self._publisher = publisher
        self._tasks: set[asyncio.Task[None]] = set()

    @property
    def pending(self) -> int:
        return len(self._tasks)

    async def execute(
        self,
        *,
        link_id: int,
        user_agent: str | None,
        country: str | None,
        referrer: str | None,
    ) -> None:
        user_agent_info = parse_user_agent(user_agent)
        event = ClickEvent(
            link_id=link_id,
            clicked_at=self._clock.now(),
            country=normalize_country(country),
            device=user_agent_info.device,
            browser=user_agent_info.browser,
            referrer_host=extract_referrer_host(referrer),
        )
        task = asyncio.create_task(self._publish(event))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def _publish(self, event: ClickEvent) -> None:
        with suppress(Exception):
            await self._publisher.publish(event)

    async def drain(self) -> None:
        if not self._tasks:
            return
        await asyncio.gather(*tuple(self._tasks), return_exceptions=True)
