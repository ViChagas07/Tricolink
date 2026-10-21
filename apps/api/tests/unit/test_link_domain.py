from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from tricolink.modules.links.domain.entities import Link, LinkState
from tricolink.modules.links.domain.errors import InvalidShortCodeError, InvalidUrlError
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode


def test_short_code_accepts_valid_values() -> None:
    for value in ("abc", "A1_-z", "a" * 32, "abcDEF123_-"):
        assert ShortCode(value).value == value
    assert str(ShortCode("abc")) == "abc"


def test_original_url_rejects_non_string_and_port_zero() -> None:
    with pytest.raises(InvalidUrlError):
        OriginalUrl.parse(123)  # type: ignore[arg-type]
    with pytest.raises(InvalidUrlError):
        OriginalUrl.parse("http://example.com:0/")


@pytest.mark.parametrize(
    "value",
    [
        "http://[::1::2]/",
        "https://" + "a" * 250 + ".com/",
        "https://a..example.com/",
        "https://exa!mple.com/",
    ],
)
def test_original_url_rejects_invalid_host_shapes(value: str) -> None:
    with pytest.raises(InvalidUrlError):
        OriginalUrl.parse(value)


@pytest.mark.parametrize(
    "value",
    ["", "ab", "a" * 33, "ab c", "abc/def", "abc.def", "abc def", "ábc", "../etc"],
)
def test_short_code_rejects_invalid_values(value: str) -> None:
    with pytest.raises(InvalidShortCodeError):
        ShortCode(value)


def test_reserved_aliases_are_case_insensitive() -> None:
    assert ShortCode.is_reserved("login")
    assert ShortCode.is_reserved("LOGIN")
    assert ShortCode.is_reserved("pt-br")
    assert not ShortCode.is_reserved("not-reserved-code")


def test_original_url_normalizes_scheme_host_and_idn() -> None:
    normalized = OriginalUrl.parse("  HTTPS://Example.COM:8443/Path?Q=1#Frag  ")
    assert normalized.value == "https://example.com:8443/Path?Q=1#Frag"
    assert normalized.hostname == "example.com"


def test_original_url_normalizes_idn_to_punycode() -> None:
    normalized = OriginalUrl.parse("https://münich.example/straße")
    assert normalized.hostname == "xn--mnich-kva.example"
    assert normalized.value.startswith("https://xn--mnich-kva.example/")


def test_original_url_keeps_ipv6_literal_brackets() -> None:
    normalized = OriginalUrl.parse("https://[2606:4700:4700::1111]/x")
    assert normalized.is_ip_literal is True
    assert normalized.value == "https://[2606:4700:4700::1111]/x"


def test_original_url_strips_trailing_dot_from_host() -> None:
    assert OriginalUrl.parse("https://example.com./a").hostname == "example.com"


@pytest.mark.parametrize(
    "value",
    [
        "",
        "example.com",
        "//example.com",
        "javascript:alert(1)",
        "data:text/html,hi",
        "file:///etc/passwd",
        "ftp://example.com",
        "http://",
        "http:///path",
        "http://user:pass@example.com",
        "http://user@example.com",
        "http://localhost",
        "http://exa mple.com",
        "http://example.com:bad",
        "http://example.com:99999",
        "http://-bad.example",
        "http://exa_mple.com",
        "http://intranet",
        "https://example.com/\x00",
        "https://example.com/\u202e",
        "https://example.com/%0d%0a",
        "https://example.com/%5c",
        "https://example.com\\@evil.com",
        "https://example.com/" + "a" * 2049,
    ],
)
def test_original_url_rejects_malformed_or_dangerous_values(value: str) -> None:
    with pytest.raises(InvalidUrlError):
        OriginalUrl.parse(value)


def test_link_state_accounts_for_expiry_and_active_flag() -> None:
    now = datetime.now(UTC)
    link = Link(
        id=1,
        code=ShortCode("abc1234"),
        original_url=OriginalUrl.parse("https://93.184.216.34/"),
        title=None,
        user_id=uuid4(),
        is_custom_alias=False,
        is_active=True,
        expires_at=now + timedelta(days=1),
        click_count=0,
        created_at=now,
        updated_at=now,
    )

    assert link.state(now) is LinkState.ACTIVE
    assert link.state(now + timedelta(days=1)) is LinkState.EXPIRED

    inactive = Link(
        id=2,
        code=ShortCode("abc1235"),
        original_url=OriginalUrl.parse("https://93.184.216.34/"),
        title=None,
        user_id=None,
        is_custom_alias=False,
        is_active=False,
        expires_at=None,
        click_count=0,
        created_at=now,
        updated_at=now,
    )
    assert inactive.state(now) is LinkState.INACTIVE

    naive_now = datetime.now()
    assert link.state(naive_now) is LinkState.ACTIVE
    assert inactive.state(naive_now) is LinkState.INACTIVE


def test_link_with_updates_returns_a_new_entity() -> None:
    now = datetime.now(UTC)
    link = Link(
        id=1,
        code=ShortCode("abc1234"),
        original_url=OriginalUrl.parse("https://93.184.216.34/"),
        title=None,
        user_id=None,
        is_custom_alias=False,
        is_active=True,
        expires_at=None,
        click_count=0,
        created_at=now,
        updated_at=now,
    )
    updated = link.with_updates(
        title="new",
        original_url=OriginalUrl.parse("https://1.1.1.1/"),
        is_active=False,
        expires_at=now + timedelta(days=2),
        updated_at=now + timedelta(seconds=1),
    )

    assert updated.title == "new"
    assert updated.original_url.hostname == "1.1.1.1"
    assert updated.is_active is False
    assert updated.expires_at is not None
    assert link.title is None
