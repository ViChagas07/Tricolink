from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from urllib.parse import urlsplit

Device = Literal["desktop", "mobile", "tablet", "bot", "unknown"]

_BOT_PATTERN = re.compile(
    r"bot|crawler|spider|slurp|bingpreview|facebookexternalhit|headless",
    re.IGNORECASE,
)
_MOBILE_PATTERN = re.compile(
    r"mobile|iphone|ipod|windows phone|android.+mobile",
    re.IGNORECASE,
)
_TABLET_PATTERN = re.compile(r"ipad|tablet|kindle|silk", re.IGNORECASE)
_COUNTRY_PATTERN = re.compile(r"^[A-Za-z]{2}$")


@dataclass(frozen=True, slots=True)
class UserAgentInfo:
    device: Device
    browser: str | None


@dataclass(frozen=True, slots=True)
class ClickEvent:
    link_id: int
    clicked_at: datetime
    country: str | None
    device: Device
    browser: str | None
    referrer_host: str | None


def parse_user_agent(value: str | None) -> UserAgentInfo:
    if not value:
        return UserAgentInfo(device="unknown", browser=None)

    if _BOT_PATTERN.search(value):
        return UserAgentInfo(device="bot", browser=None)

    if _TABLET_PATTERN.search(value) or (
        "android" in value.lower() and "mobile" not in value.lower()
    ):
        device: Device = "tablet"
    elif _MOBILE_PATTERN.search(value):
        device = "mobile"
    elif "mozilla/" in value.lower():
        device = "desktop"
    else:
        device = "unknown"

    return UserAgentInfo(device=device, browser=_browser(value))


def _browser(value: str) -> str | None:
    if "Edg/" in value:
        return "edge"
    if "OPR/" in value or "Opera" in value:
        return "opera"
    if "Chrome/" in value or "CriOS/" in value:
        return "chrome"
    if "Firefox/" in value or "FxiOS/" in value:
        return "firefox"
    if "Safari/" in value:
        return "safari"
    return None


def normalize_country(value: str | None) -> str | None:
    if value is None:
        return None
    candidate = value.strip()
    if not _COUNTRY_PATTERN.fullmatch(candidate):
        return None
    return candidate.upper()


def extract_referrer_host(value: str | None) -> str | None:
    if not value:
        return None
    if any(char.isspace() or unicodedata.category(char)[0] == "C" for char in value):
        return None
    try:
        host = urlsplit(value).hostname
    except ValueError:
        return None
    if not host:
        return None
    host = host.lower().rstrip(".")
    if not host or len(host) > 255:
        return None
    return host
