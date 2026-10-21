from __future__ import annotations

import ipaddress
import re
import unicodedata
from dataclasses import dataclass
from urllib.parse import urlsplit

from tricolink.modules.links.domain.errors import InvalidShortCodeError, InvalidUrlError
from tricolink.modules.links.domain.reserved_aliases import RESERVED_ALIASES

SHORT_CODE_PATTERN = re.compile(r"^[A-Za-z0-9_-]{3,32}$")
MAX_URL_LENGTH = 2048
_ENCODED_DANGEROUS = re.compile(r"%(?:0[0-9a-f]|1[0-9a-f]|7f|5c)", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class ShortCode:
    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str) or not SHORT_CODE_PATTERN.fullmatch(self.value):
            raise InvalidShortCodeError("Short code must match ^[A-Za-z0-9_-]{3,32}$")

    @staticmethod
    def is_reserved(value: str) -> bool:
        return value.strip().lower() in RESERVED_ALIASES

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class OriginalUrl:
    value: str
    hostname: str
    is_ip_literal: bool

    @classmethod
    def parse(cls, raw: str) -> OriginalUrl:
        if not isinstance(raw, str):
            raise InvalidUrlError("URL must be a string")

        candidate = raw.strip()
        if not candidate:
            raise InvalidUrlError("URL is required")
        if len(candidate) > MAX_URL_LENGTH:
            raise InvalidUrlError(f"URL must not exceed {MAX_URL_LENGTH} characters")
        if "\\" in candidate:
            raise InvalidUrlError("URL must not contain backslashes")
        if _ENCODED_DANGEROUS.search(candidate):
            raise InvalidUrlError("URL must not contain encoded control characters")

        for char in candidate:
            if char.isspace() or unicodedata.category(char)[0] == "C":
                raise InvalidUrlError("URL must not contain control or whitespace characters")

        try:
            parts = urlsplit(candidate)
            port = parts.port
        except ValueError as exc:
            raise InvalidUrlError("URL is malformed") from exc

        scheme = parts.scheme.lower()
        if scheme not in {"http", "https"}:
            raise InvalidUrlError("URL scheme must be http or https")
        if not parts.netloc or parts.hostname is None:
            raise InvalidUrlError("URL must include a host")
        if parts.username is not None or parts.password is not None:
            raise InvalidUrlError("URL must not include credentials")
        if port == 0:
            raise InvalidUrlError("URL port is not allowed")

        raw_host = parts.hostname.strip().lower().rstrip(".")
        host, is_ip_literal = _normalize_host(raw_host)
        _validate_hostname(host, is_ip_literal=is_ip_literal)

        netloc = f"[{host}]" if ":" in host else host
        if port is not None:
            netloc = f"{netloc}:{port}"

        normalized = f"{scheme}://{netloc}{parts.path}"
        if parts.query:
            normalized = f"{normalized}?{parts.query}"
        if parts.fragment:
            normalized = f"{normalized}#{parts.fragment}"

        if len(normalized) > MAX_URL_LENGTH:
            raise InvalidUrlError(f"URL must not exceed {MAX_URL_LENGTH} characters")

        return cls(value=normalized, hostname=host, is_ip_literal=is_ip_literal)


def _normalize_host(raw_host: str) -> tuple[str, bool]:
    if not raw_host:
        raise InvalidUrlError("URL must include a host")

    if ":" in raw_host:
        try:
            address = ipaddress.IPv6Address(raw_host)
        except ValueError as exc:
            raise InvalidUrlError("URL host is not a valid IPv6 address") from exc
        return address.compressed, True

    try:
        return ipaddress.IPv4Address(raw_host).compressed, True
    except ValueError:
        pass

    if "_" in raw_host:
        raise InvalidUrlError("URL host is not valid")

    try:
        ascii_host = raw_host.encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise InvalidUrlError("URL host is not valid IDN") from exc

    return ascii_host.rstrip("."), False


def _validate_hostname(host: str, *, is_ip_literal: bool) -> None:
    if is_ip_literal:
        return
    if not host or len(host) > 253:
        raise InvalidUrlError("URL host is too long")
    labels = host.split(".")
    if len(labels) < 2:
        raise InvalidUrlError("URL host must be fully qualified")
    for label in labels:
        if not label or len(label) > 63:
            raise InvalidUrlError("URL host has an invalid label")
        if label.startswith("-") or label.endswith("-"):
            raise InvalidUrlError("URL host has an invalid label")
        if not re.fullmatch(r"[a-z0-9-]+", label):
            raise InvalidUrlError("URL host has invalid characters")
