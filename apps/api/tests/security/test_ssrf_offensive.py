from __future__ import annotations

import pytest

from tricolink.modules.links.domain.errors import InvalidUrlError
from tricolink.modules.links.domain.url_policy import HostResolutionError, UrlPolicy


class FakeResolver:
    def __init__(self, mapping: dict[str, list[str]]) -> None:
        self.mapping = mapping
        self.calls: list[str] = []

    async def resolve(self, host: str) -> list[str]:
        self.calls.append(host)
        answers = self.mapping.get(host)
        if answers is None:
            raise HostResolutionError(host)
        if answers == ["<error>"]:
            raise HostResolutionError(host)
        return answers


def policy(mapping: dict[str, list[str]] | None = None) -> tuple[UrlPolicy, FakeResolver]:
    resolver = FakeResolver(mapping or {})
    return (
        UrlPolicy(resolver=resolver, own_hosts=("tricolink.example", "www.tricolink.example")),
        resolver,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value",
    [
        "http://127.0.0.1/",
        "http://127.0.0.2/",
        "http://10.0.0.1/",
        "http://172.16.0.1/",
        "http://172.31.255.255/",
        "http://192.168.1.1/",
        "http://169.254.169.254/latest/meta-data/",
        "http://100.64.0.1/",
        "http://0.0.0.0/",
        "http://224.0.0.1/",
        "http://240.0.0.1/",
        "http://[::1]/",
        "http://[::]/",
        "http://[fe80::1]/",
        "http://[fc00::1]/",
        "http://[fd00::1]/",
        "http://[::ffff:127.0.0.1]/",
        "http://[::ffff:7f00:1]/",
        "http://[0:0:0:0:0:ffff:127.0.0.1]/",
    ],
)
async def test_private_loopback_and_metadata_ip_literals_are_blocked(value: str) -> None:
    validator, resolver = policy()

    with pytest.raises(InvalidUrlError):
        await validator.validate(value)

    assert resolver.calls == []


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("value", "mapping"),
    [
        ("http://2130706433/", {}),
        ("http://0177.0.0.1/", {"0177.0.0.1": ["127.0.0.1"]}),
        ("http://0x7f.0.0.1/", {"0x7f.0.0.1": ["127.0.0.1"]}),
        ("http://0x7f000001/", {}),
        ("http://127.1/", {"127.1": ["127.0.0.1"]}),
        ("http://127.0.0.1.nip.io/", {"127.0.0.1.nip.io": ["127.0.0.1"]}),
        ("http://localtest.me/", {"localtest.me": ["127.0.0.1"]}),
        ("http://169.254.169.254.nip.io/", {"169.254.169.254.nip.io": ["169.254.169.254"]}),
        ("http://metadata.google.internal/", {}),
        ("http://0/", {}),
    ],
)
async def test_obfuscated_or_internal_hostnames_are_blocked(
    value: str,
    mapping: dict[str, list[str]],
) -> None:
    validator, _ = policy(mapping)

    with pytest.raises(InvalidUrlError):
        await validator.validate(value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "answers",
    [
        ["93.184.216.34", "10.0.0.5"],
        ["10.0.0.5", "93.184.216.34"],
        ["93.184.216.34", "169.254.169.254"],
        ["93.184.216.34", "2606:4700:4700::1111", "::1"],
    ],
)
async def test_dns_rebinding_mixed_answers_are_all_checked(answers: list[str]) -> None:
    validator, resolver = policy({"rebind.example": answers})

    with pytest.raises(InvalidUrlError):
        await validator.validate("https://rebind.example/path")

    assert resolver.calls == ["rebind.example"]


@pytest.mark.asyncio
async def test_own_domain_and_subdomains_are_blocked_as_redirect_loops() -> None:
    validator, resolver = policy()

    for value in (
        "https://tricolink.example/",
        "https://sub.tricolink.example/",
        "https://TRICOLINK.EXAMPLE./",
        "https://münich.tricolink.example/",
    ):
        with pytest.raises(InvalidUrlError):
            await validator.validate(value)

    assert resolver.calls == []


@pytest.mark.asyncio
async def test_public_hosts_near_the_own_domain_are_allowed() -> None:
    validator, _ = policy({"not-tricolink.example": ["93.184.216.34"]})

    normalized = await validator.validate("https://not-tricolink.example/path")

    assert normalized.hostname == "not-tricolink.example"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value",
    [
        "javascript:alert(1)",
        "data:text/html,<script>alert(1)</script>",
        "file:///etc/passwd",
        "ftp://example.com/file",
        "gopher://127.0.0.1:6379/_INFO",
        "ws://example.com/socket",
        "wss://example.com/socket",
        "chrome://settings/",
        "about:blank",
        "//evil.example/path",
    ],
)
async def test_forbidden_schemes_and_scheme_relative_urls_are_blocked(value: str) -> None:
    validator, _ = policy()

    with pytest.raises(InvalidUrlError):
        await validator.validate(value)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value",
    [
        "http://user:pass@example.com/",
        "http://user@example.com/",
        "https://example.com\\@evil.example/",
        "https://example.com/%0d%0aLocation:%20https://evil.example",
        "https://example.com/%5c",
        "https://example.com/\x00",
        "https://example.com/\u202e",
        "https://exa mple.com/",
    ],
)
async def test_credentials_controls_and_backslashes_are_blocked(value: str) -> None:
    validator, _ = policy({"example.com": ["93.184.216.34"]})

    with pytest.raises(InvalidUrlError):
        await validator.validate(value)


@pytest.mark.asyncio
async def test_resolution_failures_and_empty_answers_are_blocked() -> None:
    validator, _ = policy(
        {
            "down.example": ["<error>"],
            "empty.example": [],
            "garbage.example": ["not-an-ip"],
        }
    )

    for value in (
        "https://down.example/",
        "https://empty.example/",
        "https://garbage.example/",
        "https://unlisted.example/",
    ):
        with pytest.raises(InvalidUrlError):
            await validator.validate(value)


@pytest.mark.asyncio
async def test_global_ipv4_and_ipv6_answers_are_accepted() -> None:
    validator, _ = policy(
        {
            "v4.example": ["93.184.216.34"],
            "v6.example": ["2606:4700:4700::1111"],
            "dual.example": ["93.184.216.34", "2606:4700:4700::1111"],
        }
    )

    for value in (
        "https://v4.example/",
        "https://v6.example/",
        "https://dual.example/",
    ):
        assert (await validator.validate(value)).value
