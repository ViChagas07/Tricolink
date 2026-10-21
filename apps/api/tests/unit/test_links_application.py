from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from tricolink.modules.analytics.domain.click import ClickEvent
from tricolink.modules.links.application import (
    UNSET,
    AliasReserved,
    AliasTaken,
    CacheEntry,
    CacheUnavailable,
    CodeGenerationFailed,
    CreateLink,
    CreateLinkCommand,
    DailyQuotaExceeded,
    DeleteLink,
    GetLink,
    InvalidCursor,
    InvalidPagination,
    LinkNotFound,
    ListLinks,
    LoginRequired,
    RecordClick,
    ResolveLink,
    UpdateLink,
    UpdateLinkCommand,
    UrlNotAllowed,
)
from tricolink.modules.links.application.pagination import decode_cursor, encode_cursor
from tricolink.modules.links.domain.code_generator import CodeGenerator
from tricolink.modules.links.domain.entities import Link, LinkState
from tricolink.modules.links.domain.errors import DuplicateCodeError
from tricolink.modules.links.domain.url_policy import UrlPolicy
from tricolink.modules.links.domain.value_objects import OriginalUrl, ShortCode

NOW = datetime(2026, 10, 21, 12, 0, tzinfo=UTC)


class FakeClock:
    def __init__(self, now: datetime = NOW) -> None:
        self.value = now

    def now(self) -> datetime:
        return self.value


class FakeResolver:
    async def resolve(self, host: str) -> list[str]:
        return ["93.184.216.34"]


class FakeQuota:
    def __init__(self, allowed: bool = True, retry_after: int = 10) -> None:
        self.allowed = allowed
        self.retry_after = retry_after
        self.calls: list[tuple[str, str, int]] = []

    async def consume(self, scope: str, key: str, limit: int) -> object:
        from tricolink.modules.links.application.ports import QuotaResult

        self.calls.append((scope, key, limit))
        return QuotaResult(
            allowed=self.allowed,
            used=0 if self.allowed else limit,
            limit=limit,
            retry_after_seconds=self.retry_after,
        )


class FakeRepository:
    def __init__(self) -> None:
        self.links: dict[str, Link] = {}
        self.create_calls: list[str] = []
        self.fail_codes: list[str] = []
        self.next_id = 1
        self.get_by_code_calls = 0

    async def create(self, link: Link) -> Link:
        self.create_calls.append(link.code.value)
        if link.code.value in self.fail_codes:
            self.fail_codes.remove(link.code.value)
            raise DuplicateCodeError(link.code.value)
        created = replace(link, id=self.next_id)
        self.next_id += 1
        self.links[link.code.value] = created
        return created

    async def get_by_code(self, code: ShortCode) -> Link | None:
        self.get_by_code_calls += 1
        return self.links.get(code.value)

    async def get_for_user(self, code: ShortCode, user_id: UUID) -> Link | None:
        link = self.links.get(code.value)
        return link if link is not None and link.user_id == user_id else None

    async def list_for_user(
        self,
        user_id: UUID,
        *,
        cursor: object,
        limit: int,
        query: str | None,
    ) -> list[Link]:
        rows = [link for link in self.links.values() if link.user_id == user_id]
        if query:
            rows = [
                link
                for link in rows
                if query.lower() in link.code.value.lower()
                or (link.title and query.lower() in link.title.lower())
            ]
        rows.sort(key=lambda link: (link.created_at, link.id or 0), reverse=True)
        if cursor is not None:
            assert cursor.link_id
            rows = [
                link
                for link in rows
                if (link.created_at, link.id or 0) < (cursor.created_at, cursor.link_id)  # type: ignore[attr-defined]
            ]
        return rows[:limit]

    async def update(self, link: Link, user_id: UUID) -> Link | None:
        current = self.links.get(link.code.value)
        if current is None or current.user_id != user_id:
            return None
        self.links[link.code.value] = link
        return link

    async def delete(self, code: ShortCode, user_id: UUID) -> bool:
        current = self.links.get(code.value)
        if current is None or current.user_id != user_id:
            return False
        del self.links[code.value]
        return True


class FakeCache:
    def __init__(self, unavailable: bool = False) -> None:
        self.entries: dict[str, CacheEntry] = {}
        self.invalidated: list[str] = []
        self.unavailable = unavailable

    async def resolve(self, code: ShortCode, loader: object) -> CacheEntry | None:
        if self.unavailable:
            raise CacheUnavailable()
        if code.value in self.entries:
            return self.entries[code.value]
        link = await loader()  # type: ignore[operator]
        if link is None:
            return None
        entry = CacheEntry(
            link_id=link.id or 0,
            original_url=link.original_url.value,
            expires_at=link.expires_at,
            is_active=link.is_active,
        )
        self.entries[code.value] = entry
        return entry

    async def invalidate(self, code: ShortCode) -> None:
        self.invalidated.append(code.value)
        self.entries.pop(code.value, None)


class FakeGenerator:
    def __init__(self, values: list[str]) -> None:
        self.values = list(values)

    def generate(self) -> str:
        return self.values.pop(0)


class FakePublisher:
    def __init__(self, *, block: bool = False) -> None:
        self.block = block
        self.release = asyncio.Event()
        self.events: list[ClickEvent] = []

    async def publish(self, event: ClickEvent) -> bool:
        if self.block:
            await self.release.wait()
        self.events.append(event)
        return True


def build_link(
    *,
    code: str = "abc1234",
    user_id: UUID | None = None,
    expires_at: datetime | None = None,
    is_active: bool = True,
    created_at: datetime = NOW,
    title: str | None = None,
) -> Link:
    return Link(
        id=None,
        code=ShortCode(code),
        original_url=OriginalUrl.parse("https://93.184.216.34/path"),
        title=title,
        user_id=user_id,
        is_custom_alias=False,
        is_active=is_active,
        expires_at=expires_at,
        click_count=0,
        created_at=created_at,
        updated_at=created_at,
    )


def build_create(
    *,
    clock: FakeClock | None = None,
    repository: FakeRepository | None = None,
    cache: FakeCache | None = None,
    quota: FakeQuota | None = None,
    generator: FakeGenerator | None = None,
    policy: UrlPolicy | None = None,
) -> CreateLink:
    return CreateLink(
        repository=repository or FakeRepository(),
        cache=cache or FakeCache(),
        url_policy=policy or UrlPolicy(resolver=FakeResolver()),
        code_generator=generator or CodeGenerator(),
        quota=quota or FakeQuota(),
        clock=clock or FakeClock(),
        anon_daily_limit=5,
        user_daily_limit=100,
        anon_ttl_days=30,
    )


@pytest.mark.asyncio
async def test_create_anonymous_sets_expiry_and_uses_ip_quota() -> None:
    repository = FakeRepository()
    cache = FakeCache()
    quota = FakeQuota()
    use_case = build_create(repository=repository, cache=cache, quota=quota)

    link = await use_case.execute(
        CreateLinkCommand(
            url="https://93.184.216.34/path",
            user_id=None,
            client_ip="203.0.113.5",
        )
    )

    assert link.user_id is None
    assert link.expires_at == NOW + timedelta(days=30)
    assert len(link.code.value) == 7
    assert quota.calls == [("anon", "203.0.113.5", 5)]
    assert cache.invalidated == [link.code.value]


@pytest.mark.asyncio
async def test_create_anonymous_cannot_use_logged_only_fields() -> None:
    use_case = build_create()

    for field in (
        {"alias": "custom-alias"},
        {"title": "A title"},
        {"expires_at": NOW + timedelta(days=1)},
    ):
        with pytest.raises(LoginRequired):
            await use_case.execute(
                CreateLinkCommand(
                    url="https://93.184.216.34/",
                    user_id=None,
                    client_ip="203.0.113.5",
                    **field,
                )
            )


@pytest.mark.asyncio
async def test_create_logged_with_alias_and_title() -> None:
    user_id = uuid4()
    quota = FakeQuota()
    use_case = build_create(quota=quota)

    link = await use_case.execute(
        CreateLinkCommand(
            url="https://93.184.216.34/path",
            user_id=user_id,
            client_ip="203.0.113.5",
            alias="my-alias",
            title=" My title ",
            expires_at=NOW + timedelta(days=2),
        )
    )

    assert link.code.value == "my-alias"
    assert link.is_custom_alias is True
    assert link.title == "My title"
    assert link.user_id == user_id
    assert quota.calls == [("user", str(user_id), 100)]


@pytest.mark.asyncio
async def test_create_rejects_reserved_or_duplicate_alias() -> None:
    user_id = uuid4()
    use_case = build_create()

    with pytest.raises(AliasReserved):
        await use_case.execute(
            CreateLinkCommand(
                url="https://93.184.216.34/",
                user_id=user_id,
                client_ip="ip",
                alias="login",
            )
        )

    repository = FakeRepository()
    repository.fail_codes.append("taken-alias")
    use_case = build_create(repository=repository)

    with pytest.raises(AliasTaken):
        await use_case.execute(
            CreateLinkCommand(
                url="https://93.184.216.34/",
                user_id=user_id,
                client_ip="ip",
                alias="taken-alias",
            )
        )


@pytest.mark.asyncio
async def test_create_retries_code_collisions() -> None:
    repository = FakeRepository()
    repository.fail_codes.extend(["AAAAAAA", "AAAAAAA"])
    generator = FakeGenerator(["AAAAAAA", "AAAAAAA", "BBBBBBB"])
    use_case = build_create(repository=repository, generator=generator)

    link = await use_case.execute(
        CreateLinkCommand(url="https://93.184.216.34/", user_id=None, client_ip="ip")
    )

    assert link.code.value == "BBBBBBB"
    assert repository.create_calls == ["AAAAAAA", "AAAAAAA", "BBBBBBB"]


@pytest.mark.asyncio
async def test_create_fails_after_five_collisions() -> None:
    repository = FakeRepository()
    repository.fail_codes.extend(["AAAAAAA"] * 5)
    generator = FakeGenerator(["AAAAAAA"] * 5)
    use_case = build_create(repository=repository, generator=generator)

    with pytest.raises(CodeGenerationFailed):
        await use_case.execute(
            CreateLinkCommand(url="https://93.184.216.34/", user_id=None, client_ip="ip")
        )


@pytest.mark.asyncio
async def test_create_enforces_daily_quota_and_url_policy() -> None:
    use_case = build_create(quota=FakeQuota(allowed=False, retry_after=42))

    with pytest.raises(DailyQuotaExceeded) as quota_error:
        await use_case.execute(
            CreateLinkCommand(url="https://93.184.216.34/", user_id=None, client_ip="ip")
        )
    assert quota_error.value.headers == {"Retry-After": "42"}

    with pytest.raises(UrlNotAllowed):
        await use_case.execute(
            CreateLinkCommand(url="http://127.0.0.1/", user_id=None, client_ip="ip")
        )


@pytest.mark.asyncio
async def test_update_changes_url_and_invalidates_cache() -> None:
    user_id = uuid4()
    repository = FakeRepository()
    cache = FakeCache()
    created = await repository.create(build_link(user_id=user_id))
    use_case = UpdateLink(
        repository=repository,
        cache=cache,
        url_policy=UrlPolicy(resolver=FakeResolver()),
        clock=FakeClock(),
    )

    updated = await use_case.execute(
        UpdateLinkCommand(
            code=created.code.value,
            user_id=user_id,
            original_url="https://93.184.216.34/new",
            title="new title",
            expires_at=UNSET,
        )
    )

    assert updated.original_url.value == "https://93.184.216.34/new"
    assert updated.title == "new title"
    assert cache.invalidated == [created.code.value]


@pytest.mark.asyncio
async def test_update_and_delete_are_owner_only() -> None:
    owner = uuid4()
    other = uuid4()
    repository = FakeRepository()
    cache = FakeCache()
    created = await repository.create(build_link(user_id=owner))
    updater = UpdateLink(
        repository=repository,
        cache=cache,
        url_policy=UrlPolicy(resolver=FakeResolver()),
        clock=FakeClock(),
    )

    with pytest.raises(LinkNotFound):
        await updater.execute(UpdateLinkCommand(code=created.code.value, user_id=other, title="x"))
    with pytest.raises(LinkNotFound):
        await DeleteLink(repository=repository, cache=cache).execute(created.code.value, other)
    assert created.code.value in repository.links

    await DeleteLink(repository=repository, cache=cache).execute(created.code.value, owner)
    assert created.code.value not in repository.links
    assert cache.invalidated == [created.code.value]


@pytest.mark.asyncio
async def test_get_and_list_use_cursor_pagination() -> None:
    user_id = uuid4()
    repository = FakeRepository()
    for index in range(3):
        await repository.create(
            build_link(
                code=f"code{index:03d}",
                user_id=user_id,
                created_at=NOW - timedelta(minutes=index),
            )
        )

    lister = ListLinks(repository=repository)
    first = await lister.execute(user_id=user_id, cursor=None, limit=2, query=None)
    assert len(first.items) == 2
    assert first.next_cursor is not None

    second = await lister.execute(user_id=user_id, cursor=first.next_cursor, limit=2, query=None)
    assert len(second.items) == 1
    assert second.next_cursor is None
    assert {item.code.value for item in first.items}.isdisjoint(
        {item.code.value for item in second.items}
    )

    with pytest.raises(InvalidCursor):
        await lister.execute(user_id=user_id, cursor="not-base64!", limit=2, query=None)
    with pytest.raises(InvalidPagination):
        await lister.execute(user_id=user_id, cursor=None, limit=51, query=None)
    with pytest.raises(InvalidPagination):
        await lister.execute(user_id=user_id, cursor=None, limit=2, query="\x00")


@pytest.mark.asyncio
async def test_get_link_returns_owner_link_or_404() -> None:
    user_id = uuid4()
    repository = FakeRepository()
    created = await repository.create(build_link(user_id=user_id))
    getter = GetLink(repository=repository)

    assert (await getter.execute(created.code.value, user_id)).code == created.code

    with pytest.raises(LinkNotFound):
        await getter.execute(created.code.value, uuid4())
    with pytest.raises(LinkNotFound):
        await getter.execute("bad code", user_id)


def test_cursor_roundtrip_and_rejection() -> None:
    link = replace(build_link(), id=12)
    cursor = encode_cursor(link)
    decoded = decode_cursor(cursor)

    assert decoded.link_id == 12
    assert decoded.created_at == NOW

    for value in ("", "abc", "not-base64!", "bm8tc2VwYXJhdG9y"):
        with pytest.raises(InvalidCursor):
            decode_cursor(value)


@pytest.mark.asyncio
async def test_resolve_handles_cache_states_and_fallback() -> None:
    now = NOW
    active = build_link(code="active1", expires_at=now + timedelta(days=1))
    expired = build_link(code="expired", expires_at=now - timedelta(seconds=1))
    inactive = build_link(code="inactive", is_active=False)
    repository = FakeRepository()
    for link in (active, expired, inactive):
        await repository.create(link)

    cache = FakeCache()
    resolver = ResolveLink(repository=repository, cache=cache, clock=FakeClock(now))

    resolved = await resolver.execute(active.code.value)
    assert resolved is not None
    assert resolved.state is LinkState.ACTIVE

    assert (await resolver.execute(expired.code.value)).state is LinkState.EXPIRED
    assert (await resolver.execute(inactive.code.value)).state is LinkState.INACTIVE
    assert await resolver.execute("missing-x") is None
    assert await resolver.execute("bad code") is None

    fallback_repo = FakeRepository()
    await fallback_repo.create(active)
    fallback = ResolveLink(
        repository=fallback_repo,
        cache=FakeCache(unavailable=True),
        clock=FakeClock(now),
    )
    assert (await fallback.execute(active.code.value)).state is LinkState.ACTIVE


@pytest.mark.asyncio
async def test_record_click_never_blocks_and_strips_sensitive_data() -> None:
    publisher = FakePublisher(block=True)
    recorder = RecordClick(clock=FakeClock(), publisher=publisher)

    await recorder.execute(
        link_id=7,
        user_agent=(
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) "
            "AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1"
        ),
        country="br",
        referrer="https://news.example.com/path?q=secret",
    )

    assert recorder.pending == 1
    assert publisher.events == []

    publisher.release.set()
    await recorder.drain()

    event = publisher.events[0]
    assert event.link_id == 7
    assert event.country == "BR"
    assert event.device == "mobile"
    assert event.browser == "safari"
    assert event.referrer_host == "news.example.com"
    assert "iPhone" not in repr(event)
    assert "secret" not in repr(event)
