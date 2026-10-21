from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from tricolink.modules.links.domain.entities import Link, LinkState


@dataclass(frozen=True, slots=True)
class CreateLinkCommand:
    url: str
    user_id: UUID | None
    client_ip: str
    alias: str | None = None
    title: str | None = None
    expires_at: datetime | None = None


class _Unset:
    __slots__ = ()

    def __repr__(self) -> str:
        return "UNSET"


UNSET = _Unset()
Unset = _Unset


@dataclass(frozen=True, slots=True)
class UpdateLinkCommand:
    code: str
    user_id: UUID
    title: str | None | Unset = UNSET
    original_url: str | Unset = UNSET
    expires_at: datetime | None | Unset = UNSET
    is_active: bool | Unset = UNSET


@dataclass(frozen=True, slots=True)
class LinkPage:
    items: list[Link]
    next_cursor: str | None


@dataclass(frozen=True, slots=True)
class ResolvedLink:
    link_id: int
    original_url: str
    state: LinkState
