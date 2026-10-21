from __future__ import annotations

import asyncio
import socket

from tricolink.infra.resilience import Bulkhead
from tricolink.modules.links.domain.url_policy import HostResolutionError


class SystemHostResolver:
    """Resolves every address for a host under the DNS bulkhead."""

    def __init__(self, *, bulkhead: Bulkhead, timeout_seconds: float = 2.0) -> None:
        self._bulkhead = bulkhead
        self._timeout_seconds = timeout_seconds

    async def resolve(self, host: str) -> list[str]:
        async with self._bulkhead.acquire():
            loop = asyncio.get_running_loop()
            try:
                info = await asyncio.wait_for(
                    loop.getaddrinfo(host, None, type=socket.SOCK_STREAM),
                    timeout=self._timeout_seconds,
                )
            except (TimeoutError, socket.gaierror, OSError) as exc:
                raise HostResolutionError(host) from exc

        addresses = {str(entry[4][0]) for entry in info if entry[4]}
        return sorted(addresses)
