from __future__ import annotations

from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

_SET_RLS_CONTEXT = text(
    """
    SELECT
      set_config('app.current_user_id', :user_id, true),
      set_config('app.current_link_code', :link_code, true),
      set_config('app.refresh_token_hash', :refresh_token_hash, true),
      set_config('app.refresh_family_id', :refresh_family_id, true),
      set_config('app.click_flusher', :click_flusher, true)
    """
)


async def set_rls_context(
    session: AsyncSession,
    *,
    user_id: UUID | str | None = None,
    link_code: str | None = None,
    refresh_token_hash: str | None = None,
    refresh_family_id: UUID | str | None = None,
    click_flusher: bool = False,
) -> None:
    await session.execute(
        _SET_RLS_CONTEXT,
        {
            "user_id": str(user_id) if user_id else "",
            "link_code": link_code or "",
            "refresh_token_hash": refresh_token_hash or "",
            "refresh_family_id": str(refresh_family_id) if refresh_family_id else "",
            "click_flusher": "1" if click_flusher else "",
        },
    )
