from __future__ import annotations

from fastapi import Request

from tricolink.core.deps import get_services
from tricolink.modules.analytics.application.get_link_stats import GetLinkStats


def get_get_link_stats(request: Request) -> GetLinkStats:
    return get_services(request).analytics.get_link_stats
