from __future__ import annotations

import ipaddress
from collections.abc import Iterable
from typing import Protocol
from urllib.parse import urlsplit

from tricolink.modules.links.domain.errors import InvalidUrlError
from tricolink.modules.links.domain.value_objects import OriginalUrl

_BLOCKED_HOSTNAMES = frozenset(
    {
        "localhost",
        "localhost.localdomain",
        "ip6-localhost",
        "metadata",
        "metadata.google.internal",
    }
)


class HostResolutionError(Exception):
    """Raised when a hostname cannot be resolved safely."""


class HostResolver(Protocol):
    async def resolve(self, host: str) -> list[str]: ...


class UrlPolicy:
    """Validates URLs against the Tricolink anti-abuse policy.

    The resolver is injected so the domain stays framework-free and tests can
    simulate DNS answers, including rebinding-style mixed answers.
    """

    def __init__(
        self,
        *,
        resolver: HostResolver,
        own_hosts: Iterable[str] = (),
    ) -> None:
        self._resolver = resolver
        self._own_hosts = frozenset(
            normalized for host in own_hosts if (normalized := _normalize_own_host(host))
        )

    async def validate(self, raw_url: str) -> OriginalUrl:
        url = OriginalUrl.parse(raw_url)

        if self._is_own_host(url.hostname):
            raise InvalidUrlError("URL points to the Tricolink domain")
        if url.hostname in _BLOCKED_HOSTNAMES:
            raise InvalidUrlError("URL host is not allowed")

        if url.is_ip_literal:
            address = ipaddress.ip_address(url.hostname)
            if is_blocked_ip(address):
                raise InvalidUrlError("URL host is not a public address")
            return url

        try:
            addresses = await self._resolver.resolve(url.hostname)
        except HostResolutionError as exc:
            raise InvalidUrlError("URL host could not be resolved") from exc

        if not addresses:
            raise InvalidUrlError("URL host could not be resolved")

        for raw_address in addresses:
            try:
                address = ipaddress.ip_address(raw_address.split("%", 1)[0])
            except ValueError as exc:
                raise InvalidUrlError("URL host resolved to an invalid address") from exc
            if is_blocked_ip(address):
                raise InvalidUrlError("URL host resolves to a non-public address")

        return url

    def _is_own_host(self, host: str) -> bool:
        return any(host == own or host.endswith(f".{own}") for own in self._own_hosts)


def is_blocked_ip(address: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None:
        address = address.ipv4_mapped
    return (
        not address.is_global
        or address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
    )


def _normalize_own_host(value: str) -> str:
    candidate = value.strip().lower().rstrip(".")
    if "://" in candidate:
        try:
            candidate = urlsplit(candidate).hostname or ""
        except ValueError:
            return ""
    if not candidate:
        return ""
    try:
        return candidate.encode("idna").decode("ascii").lower().rstrip(".")
    except UnicodeError:
        return candidate
