from __future__ import annotations

import unicodedata
from uuid import UUID

from tricolink.modules.links.application.dto import LinkPage
from tricolink.modules.links.application.errors import InvalidPagination
from tricolink.modules.links.application.pagination import decode_cursor, encode_cursor
from tricolink.modules.links.application.ports import LinkRepository

MAX_LIST_LIMIT = 50
MAX_QUERY_LENGTH = 100


class ListLinks:
    def __init__(self, *, repository: LinkRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        *,
        user_id: UUID,
        cursor: str | None,
        limit: int,
        query: str | None,
    ) -> LinkPage:
        if limit < 1 or limit > MAX_LIST_LIMIT:
            raise InvalidPagination()
        parsed_cursor = decode_cursor(cursor) if cursor else None
        normalized_query = _normalize_query(query)

        rows = await self._repository.list_for_user(
            user_id,
            cursor=parsed_cursor,
            limit=limit + 1,
            query=normalized_query,
        )
        has_more = len(rows) > limit
        items = rows[:limit]
        next_cursor = encode_cursor(items[-1]) if has_more and items else None
        return LinkPage(items=items, next_cursor=next_cursor)


def _normalize_query(query: str | None) -> str | None:
    if query is None:
        return None
    normalized = query.strip()
    if not normalized:
        return None
    if len(normalized) > MAX_QUERY_LENGTH:
        raise InvalidPagination(f"Search query must not exceed {MAX_QUERY_LENGTH} characters")
    if any(unicodedata.category(char)[0] == "C" for char in normalized):
        raise InvalidPagination("Search query contains control characters")
    return normalized
