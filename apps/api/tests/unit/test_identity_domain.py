from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from tricolink.modules.identity.domain import (
    Email,
    InvalidEmailError,
    InvalidGoogleIdentityError,
    PasswordPolicy,
    RefreshTokenRecord,
    TokenFamily,
    User,
    WeakPasswordError,
    validate_google_claims,
)

NOW = datetime(2026, 10, 21, 12, 0, tzinfo=UTC)


def test_email_is_nfkc_normalized_and_lowercased() -> None:
    assert Email.parse("  ALEX@Example.COM ").value == "alex@example.com"
    assert Email.parse("ａｌｅｘ@ｅｘａｍｐｌｅ.com").value == "alex@example.com"
    assert str(Email.parse("a@example.com")) == "a@example.com"


def test_email_rejects_non_string_and_too_long() -> None:
    with pytest.raises(InvalidEmailError):
        Email.parse(123)  # type: ignore[arg-type]
    with pytest.raises(InvalidEmailError):
        Email.parse("a" * 250 + "@example.com")


@pytest.mark.parametrize(
    "value",
    ["", "no-at", "@example.com", "a@", "a b@example.com", "a@example", "a" * 250 + "@x.com"],
)
def test_email_rejects_invalid_values(value: str) -> None:
    with pytest.raises(InvalidEmailError):
        Email.parse(value)


def test_password_policy_accepts_strong_password() -> None:
    PasswordPolicy().validate("correct horse battery staple")


@pytest.mark.parametrize(
    "password",
    ["short", "password123", "qwertyuiop", "aaaaaaaaaa", "1234567890", "\x00abcdefghi"],
)
def test_password_policy_rejects_weak_passwords(password: str) -> None:
    with pytest.raises(WeakPasswordError):
        PasswordPolicy().validate(password)


def test_password_policy_rejects_email_local_part() -> None:
    with pytest.raises(WeakPasswordError):
        PasswordPolicy().validate(
            "alexandria",
            email=Email.parse("alexandria@example.com"),
        )


def test_password_policy_rejects_non_string_and_extremes() -> None:
    with pytest.raises(WeakPasswordError):
        PasswordPolicy().validate(None)  # type: ignore[arg-type]
    with pytest.raises(WeakPasswordError):
        PasswordPolicy().validate("a" * 129)
    with pytest.raises(WeakPasswordError):
        PasswordPolicy().validate("          ")


def test_refresh_record_handles_naive_datetimes() -> None:
    record = RefreshTokenRecord(
        id=uuid4(),
        user_id=uuid4(),
        family_id=uuid4(),
        token_hash="a" * 64,
        expires_at=datetime(2026, 10, 22, 12, 0),
        revoked_at=None,
        created_at=NOW,
    )
    assert record.is_expired(NOW + timedelta(days=1)) is True


def test_user_google_link_keeps_existing_display_name() -> None:
    user = User(
        id=uuid4(),
        email=Email.parse("user@example.com"),
        password_hash="$argon2id$hash",
        google_sub=None,
        display_name="Existing",
        locale="en",
        is_active=True,
        created_at=NOW,
    )

    linked = user.link_google("google-sub", "Google Name")
    assert linked.google_sub == "google-sub"
    assert linked.display_name == "Existing"
    assert linked.has_password is True
    assert linked.is_google_linked is True

    without_name = User(
        id=uuid4(),
        email=Email.parse("other@example.com"),
        password_hash=None,
        google_sub=None,
        display_name=None,
        locale=None,
        is_active=True,
        created_at=NOW,
    )
    assert without_name.link_google("sub", "Name").display_name == "Name"
    assert without_name.with_profile(display_name="New", locale="pt-BR").locale == "pt-BR"


def test_token_family_and_refresh_record_lifecycle() -> None:
    user_id = uuid4()
    family = TokenFamily.create(user_id)
    other = TokenFamily.create(user_id)
    assert family.id != other.id
    assert family.user_id == user_id

    record = RefreshTokenRecord(
        id=uuid4(),
        user_id=user_id,
        family_id=family.id,
        token_hash="a" * 64,
        expires_at=NOW + timedelta(days=1),
        revoked_at=None,
        created_at=NOW,
    )
    assert record.is_revoked is False
    assert record.is_expired(NOW) is False
    assert record.is_expired(NOW + timedelta(days=1)) is True
    assert record.revoke(NOW).is_revoked is True


def google_claims(**overrides: object) -> dict[str, object]:
    claims: dict[str, object] = {
        "iss": "https://accounts.google.com",
        "aud": "client-id",
        "exp": NOW.timestamp() + 300,
        "nonce": "expected-nonce",
        "email_verified": True,
        "email": "User@Example.com",
        "sub": "google-sub",
        "name": "Google User",
    }
    claims.update(overrides)
    return claims


def test_google_claims_validate_and_normalize() -> None:
    identity = validate_google_claims(
        google_claims(),
        expected_nonce="expected-nonce",
        client_id="client-id",
        now=NOW,
    )

    assert identity.sub == "google-sub"
    assert identity.email.value == "user@example.com"
    assert identity.email_verified is True
    assert identity.display_name == "Google User"


def test_google_claims_accept_audience_list_and_string_verified() -> None:
    identity = validate_google_claims(
        google_claims(aud=["other", "client-id"], email_verified="true"),
        expected_nonce="expected-nonce",
        client_id="client-id",
        now=NOW,
    )

    assert identity.email_verified is True


@pytest.mark.parametrize(
    "overrides",
    [
        {"nonce": "wrong"},
        {"iss": "https://evil.example"},
        {"aud": "other-client"},
        {"exp": NOW.timestamp() - 3600},
        {"email_verified": False},
        {"email_verified": "false"},
        {"sub": ""},
        {"email": "not-an-email"},
        {"name": "bad\x00name"},
        {"aud": 123},
        {"exp": "tomorrow"},
        {"name": "a" * 81},
    ],
)
def test_google_claims_reject_untrusted_values(overrides: dict[str, object]) -> None:
    with pytest.raises(InvalidGoogleIdentityError):
        validate_google_claims(
            google_claims(**overrides),
            expected_nonce="expected-nonce",
            client_id="client-id",
            now=NOW,
        )


def test_google_claims_require_nonce() -> None:
    with pytest.raises(InvalidGoogleIdentityError):
        validate_google_claims(
            google_claims(nonce=None),
            expected_nonce="expected-nonce",
            client_id="client-id",
            now=NOW,
        )
