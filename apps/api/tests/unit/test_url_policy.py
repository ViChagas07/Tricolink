import pytest

from tricolink.modules.links.domain.errors import InvalidUrlError
from tricolink.modules.links.domain.url_policy import (
    HostResolutionError,
    UrlPolicy,
    is_blocked_ip,
)


class FakeResolver:
    def __init__(self, mapping: dict[str, list[str]] | None = None) -> None:
        self.mapping = mapping or {}
        self.calls: list[str] = []

    async def resolve(self, host: str) -> list[str]:
        self.calls.append(host)
        if self.mapping.get(host) == ["<error>"]:
            raise HostResolutionError(host)
        return self.mapping.get(host, [])


def build_policy(
    mapping: dict[str, list[str]] | None = None,
    *,
    own_hosts: tuple[str, ...] = ("tricolink.example",),
) -> tuple[UrlPolicy, FakeResolver]:
    resolver = FakeResolver(mapping)
    return UrlPolicy(resolver=resolver, own_hosts=own_hosts), resolver


VALID_URLS = [
    ("https://example.com/path", {"example.com": ["93.184.216.34"]}),
    ("http://sub.example.org", {"sub.example.org": ["93.184.216.34"]}),
    (
        "https://dual.example.net/x",
        {"dual.example.net": ["93.184.216.34", "2606:4700:4700::1111"]},
    ),
    ("https://münich.example/x", {"xn--mnich-kva.example": ["93.184.216.34"]}),
    ("https://93.184.216.34/x", {}),
    ("https://[2606:4700:4700::1111]/x", {}),
    ("HTTPS://EXAMPLE.COM./x", {"example.com": ["93.184.216.34"]}),
    ("https://example.com/%20", {"example.com": ["93.184.216.34"]}),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(("value", "mapping"), VALID_URLS)
async def test_url_policy_accepts_public_urls(
    value: str,
    mapping: dict[str, list[str]],
) -> None:
    policy, _ = build_policy(mapping)

    normalized = await policy.validate(value)

    assert normalized.value


@pytest.mark.asyncio
async def test_url_policy_checks_every_resolved_address() -> None:
    policy, resolver = build_policy({"rebind.example": ["93.184.216.34", "10.0.0.5"]})

    with pytest.raises(InvalidUrlError):
        await policy.validate("https://rebind.example/")

    assert resolver.calls == ["rebind.example"]


@pytest.mark.asyncio
async def test_url_policy_resolves_hostname_once() -> None:
    policy, resolver = build_policy({"example.com": ["93.184.216.34"]})

    await policy.validate("https://example.com/a")

    assert resolver.calls == ["example.com"]


@pytest.mark.asyncio
async def test_url_policy_does_not_resolve_ip_literals() -> None:
    policy, resolver = build_policy()

    await policy.validate("https://93.184.216.34/")

    assert resolver.calls == []


@pytest.mark.asyncio
async def test_url_policy_blocks_own_domain_and_subdomains_without_dns() -> None:
    policy, resolver = build_policy(own_hosts=("tricolink.example", "www.tricolink.example"))

    for value in ("https://tricolink.example/x", "https://sub.tricolink.example/x"):
        with pytest.raises(InvalidUrlError):
            await policy.validate(value)

    assert resolver.calls == []


@pytest.mark.asyncio
async def test_url_policy_blocks_host_when_resolution_fails_or_is_empty() -> None:
    policy, _ = build_policy({"unknown.example": ["<error>"], "empty.example": []})

    with pytest.raises(InvalidUrlError):
        await policy.validate("https://unknown.example/")
    with pytest.raises(InvalidUrlError):
        await policy.validate("https://empty.example/")


@pytest.mark.asyncio
async def test_url_policy_blocks_invalid_dns_answer() -> None:
    policy, _ = build_policy({"bad.example": ["not-an-ip"]})

    with pytest.raises(InvalidUrlError):
        await policy.validate("https://bad.example/")


def test_url_policy_normalizes_own_host_variants() -> None:
    policy, _ = build_policy(
        own_hosts=(
            "https://tricolink.example/path",
            "",
            "http://[bad",
            "münich.example",
        )
    )

    assert policy._is_own_host("tricolink.example") is True
    assert policy._is_own_host("xn--mnich-kva.example") is True
    assert policy._is_own_host("other.example") is False


INVALID_URLS = [
    ("javascript:alert(1)", {}),
    ("data:text/html,hello", {}),
    ("file:///etc/passwd", {}),
    ("ftp://example.com/file", {}),
    ("http://", {}),
    ("http:///path", {}),
    ("//example.com", {}),
    ("example.com", {}),
    ("http://user:pass@example.com", {}),
    ("http://user@example.com", {}),
    ("http://localhost/", {}),
    ("http://localhost.localdomain/", {}),
    ("http://127.0.0.1/", {}),
    ("http://127.0.0.2/", {}),
    ("http://[::1]/", {}),
    ("http://169.254.169.254/latest/meta-data", {}),
    ("http://10.0.0.1/", {}),
    ("http://192.168.1.10/", {}),
    ("http://172.16.0.1/", {}),
    ("http://100.64.0.1/", {}),
    ("http://0.0.0.0/", {}),
    ("http://224.0.0.1/", {}),
    ("http://240.0.0.1/", {}),
    ("http://[fe80::1]/", {}),
    ("http://[fc00::1]/", {}),
    ("http://[::ffff:127.0.0.1]/", {}),
    ("http://metadata.google.internal/", {}),
    (
        "https://private.example/",
        {"private.example": ["10.1.2.3"]},
    ),
    (
        "https://mixed.example/",
        {"mixed.example": ["93.184.216.34", "192.168.0.2"]},
    ),
    (
        "https://empty.example/",
        {"empty.example": []},
    ),
    (
        "https://unresolved.example/",
        {"unresolved.example": ["<error>"]},
    ),
    ("https://tricolink.example/loop", {}),
    ("https://sub.tricolink.example/loop", {}),
    ("https://example.com:bad/", {}),
    ("https://example.com:99999/", {}),
    ("https://exa mple.com/", {}),
    ("https://example.com/\x00", {}),
    ("https://example.com/\u202e", {}),
    ("https://example.com/%0d%0a", {}),
    ("https://example.com/%5c", {}),
    ("https://example.com\\@evil.com/", {}),
    ("https://intranet/", {}),
    ("https://-bad.example/", {}),
    ("https://bad-.example/", {}),
    ("https://exa_mple.com/", {}),
    ("https://example.com/" + "a" * 2049, {}),
]


@pytest.mark.asyncio
@pytest.mark.parametrize(("value", "mapping"), INVALID_URLS)
async def test_url_policy_rejects_invalid_values(
    value: str,
    mapping: dict[str, list[str]],
) -> None:
    policy, _ = build_policy(mapping)

    with pytest.raises(InvalidUrlError):
        await policy.validate(value)


@pytest.mark.parametrize(
    "value",
    [
        "93.184.216.34",
        "2606:4700:4700::1111",
    ],
)
def test_is_blocked_ip_allows_only_global_addresses(value: str) -> None:
    import ipaddress

    assert is_blocked_ip(ipaddress.ip_address(value)) is False


@pytest.mark.parametrize(
    "value",
    [
        "127.0.0.1",
        "10.0.0.1",
        "172.16.0.1",
        "192.168.1.1",
        "169.254.169.254",
        "100.64.0.1",
        "::1",
        "fe80::1",
        "fc00::1",
        "::ffff:127.0.0.1",
        "0.0.0.0",
    ],
)
def test_is_blocked_ip_blocks_non_global_addresses(value: str) -> None:
    import ipaddress

    assert is_blocked_ip(ipaddress.ip_address(value)) is True
