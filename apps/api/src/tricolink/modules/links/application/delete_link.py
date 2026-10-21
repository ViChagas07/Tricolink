from __future__ import annotations

from contextlib import suppress
from uuid import UUID

from tricolink.modules.links.application.errors import LinkNotFound
from tricolink.modules.links.application.ports import CacheUnavailable, LinkCache, LinkRepository
from tricolink.modules.links.domain.errors import InvalidShortCodeError
from tricolink.modules.links.domain.value_objects import ShortCode


class DeleteLink:
    def __init__(self, *, repository: LinkRepository, cache: LinkCache) -> None:
        self._repository = repository
        self._cache = cache

    async def execute(self, code_value: str, user_id: UUID) -> None:
        try:
            code = ShortCode(code_value)
        except InvalidShortCodeError as exc:
            raise LinkNotFound() from exc

        deleted = await self._repository.delete(code, user_id)
        if not deleted:
            raise LinkNotFound()
        with suppress(CacheUnavailable):
            await self._cache.invalidate(code)
