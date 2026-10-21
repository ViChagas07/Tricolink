from __future__ import annotations

import base64
import binascii
from datetime import UTC, datetime

from tricolink.modules.links.application.errors import InvalidCursor
from tricolink.modules.links.application.ports import PageCursor
from tricolink.modules.links.domain.entities import Link

_MAX_CURSOR_LENGTH = 256


def encode_cursor(link: Link) -> str:
    if link.id is None:
        raise ValueError("Cannot build a cursor for an unsaved link")
    created_at = link.created_at.astimezone(UTC).isoformat()
    raw = f"{created_at}|{link.id}".encode()
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_cursor(value: str) -> PageCursor:
    if not value or len(value) > _MAX_CURSOR_LENGTH:
        raise InvalidCursor()
    padded = value + "=" * (-len(value) % 4)
    try:
        raw = base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8")
        created_raw, id_raw = raw.rsplit("|", 1)
        created_at = datetime.fromisoformat(created_raw)
        link_id = int(id_raw)
    except (ValueError, UnicodeError, binascii.Error) as exc:
        raise InvalidCursor() from exc

    if created_at.tzinfo is None or link_id < 1:
        raise InvalidCursor()
    return PageCursor(created_at=created_at.astimezone(UTC), link_id=link_id)
