from datetime import UTC, datetime

import pytest

from tricolink.modules.analytics.domain.click import (
    ClickEvent,
    extract_referrer_host,
    normalize_country,
    parse_user_agent,
)


@pytest.mark.parametrize(
    ("user_agent", "device", "browser"),
    [
        (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
            "AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1",
            "mobile",
            "safari",
        ),
        (
            "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 "
            "Chrome/120.0 Mobile Safari/537.36",
            "mobile",
            "chrome",
        ),
        (
            "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
            "Version/17.0 Mobile/15E148 Safari/604.1",
            "tablet",
            "safari",
        ),
        (
            "Mozilla/5.0 (Linux; Android 13; SM-X700) AppleWebKit/537.36 "
            "Chrome/120.0 Safari/537.36",
            "tablet",
            "chrome",
        ),
        ("Googlebot/2.1 (+http://www.google.com/bot.html)", "bot", None),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "Chrome/120.0 Safari/537.36",
            "desktop",
            "chrome",
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "Chrome/120.0 Safari/537.36 Edg/120.0",
            "desktop",
            "edge",
        ),
        (
            "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "desktop",
            "firefox",
        ),
        (
            "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 OPR/106.0 Safari/537.36",
            "desktop",
            "opera",
        ),
        (None, "unknown", None),
        ("", "unknown", None),
        ("curl/8.5.0", "unknown", None),
    ],
)
def test_parse_user_agent(
    user_agent: str | None,
    device: str,
    browser: str | None,
) -> None:
    info = parse_user_agent(user_agent)
    assert info.device == device
    assert info.browser == browser


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("br", "BR"),
        ("US", "US"),
        ("us", "US"),
        ("b", None),
        ("BRA", None),
        ("1A", None),
        (None, None),
    ],
)
def test_normalize_country(value: str | None, expected: str | None) -> None:
    assert normalize_country(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("https://news.example.com/path?q=1", "news.example.com"),
        ("http://Example.COM:8080/x", "example.com"),
        ("https://www.example.com/", "www.example.com"),
        ("not a url", None),
        ("", None),
        (None, None),
        ("https://example.com/\x00", None),
        ("https://" + "a" * 300 + ".com/", None),
    ],
)
def test_extract_referrer_host(value: str | None, expected: str | None) -> None:
    assert extract_referrer_host(value) == expected


def test_click_event_never_contains_raw_user_agent_or_ip() -> None:
    event = ClickEvent(
        link_id=1,
        clicked_at=datetime.now(UTC),
        country="BR",
        device="mobile",
        browser="safari",
        referrer_host="example.com",
    )

    assert set(event.__dataclass_fields__) == {
        "link_id",
        "clicked_at",
        "country",
        "device",
        "browser",
        "referrer_host",
    }
