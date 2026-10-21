from __future__ import annotations

from uuid import UUID

from tricolink.modules.links.application.errors import LinkNotFound
from tricolink.modules.links.application.ports import LinkRepository
from tricolink.modules.links.domain.entities import Link
from tricolink.modules.links.domain.errors import InvalidShortCodeError
from tricolink.modules.links.domain.value_objects import ShortCode


class GetLink:
    def __init__(self, *, repository: LinkRepository) -> None:
        self._repository = repository

    async def execute(self, code_value: str, user_id: UUID) -> Link:
        try:
            code = ShortCode(code_value)
        except InvalidShortCodeError as exc:
            raise LinkNotFound() from exc
        link = await self._repository.get_for_user(code, user_id)
        if link is None:
            raise LinkNotFound()
        return link
