from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlsplit

from redis.asyncio import Redis

from tricolink.core.config import Settings
from tricolink.infra.cache import CacheClient, close_redis, create_redis, ping_redis
from tricolink.infra.db import Database
from tricolink.infra.dns import SystemHostResolver
from tricolink.infra.ratelimit import (
    MemoryTokenBucket,
    RateLimiter,
    RedisTokenBucket,
    build_policies,
)
from tricolink.infra.ratelimit.daily_quota import RedisDailyQuota
from tricolink.infra.resilience import CircuitBreaker, build_bulkheads
from tricolink.infra.resilience.bulkhead import BulkheadRegistry
from tricolink.modules.analytics.adapters import (
    ClickFlusher,
    RedisClickPublisher,
    RedisStatsCache,
    SqlAlchemyStatsRepository,
)
from tricolink.modules.analytics.application.get_link_stats import GetLinkStats
from tricolink.modules.identity.adapters import (
    Argon2PasswordHasher,
    GoogleOIDCClient,
    PyJwtAccessTokens,
    RedisAuthThrottle,
    SqlAlchemySessionRepository,
    SqlAlchemyUserRepository,
)
from tricolink.modules.identity.application import (
    AuthenticateAccess,
    GetAvatar,
    GetMe,
    Login,
    LoginWithGoogle,
    Logout,
    RefreshSession,
    Register,
    RemoveAvatar,
    SessionIssuer,
    SetAvatar,
    UpdateMe,
)
from tricolink.modules.identity.domain import PasswordPolicy
from tricolink.modules.links.adapters import RedisLinkCache, SqlAlchemyLinkRepository
from tricolink.modules.links.application import (
    CreateLink,
    DeleteLink,
    GetLink,
    GetLinksOverview,
    ListLinks,
    RecordClick,
    ResolveLink,
    UpdateLink,
)
from tricolink.modules.links.domain import CodeGenerator, UrlPolicy
from tricolink.shared_kernel.clock import SystemClock


@dataclass(slots=True)
class AnalyticsServices:
    publisher: RedisClickPublisher
    flusher: ClickFlusher
    stats_repository: SqlAlchemyStatsRepository
    stats_cache: RedisStatsCache
    get_link_stats: GetLinkStats


@dataclass(slots=True)
class LinkServices:
    repository: SqlAlchemyLinkRepository
    cache: RedisLinkCache
    url_policy: UrlPolicy
    code_generator: CodeGenerator
    clock: SystemClock
    quota: RedisDailyQuota
    create_link: CreateLink
    get_link: GetLink
    get_overview: GetLinksOverview
    list_links: ListLinks
    update_link: UpdateLink
    delete_link: DeleteLink
    resolve_link: ResolveLink


@dataclass(slots=True)
class IdentityServices:
    users: SqlAlchemyUserRepository
    sessions: SqlAlchemySessionRepository
    hasher: Argon2PasswordHasher
    access_tokens: PyJwtAccessTokens
    throttle: RedisAuthThrottle
    google_oidc: GoogleOIDCClient
    clock: SystemClock
    register: Register
    login: Login
    refresh_session: RefreshSession
    logout: Logout
    get_me: GetMe
    update_me: UpdateMe
    get_avatar: GetAvatar
    set_avatar: SetAvatar
    remove_avatar: RemoveAvatar
    google_login: LoginWithGoogle
    authenticate_access: AuthenticateAccess


@dataclass(slots=True)
class Services:
    settings: Settings
    redis: Redis
    cache: CacheClient
    database: Database
    rate_limiter: RateLimiter
    redis_breaker: CircuitBreaker
    database_breaker: CircuitBreaker
    bulkheads: BulkheadRegistry
    links: LinkServices
    identity: IdentityServices
    analytics: AnalyticsServices
    record_click: RecordClick

    async def redis_ping(self) -> None:
        async with self.redis_breaker.guard():
            await ping_redis(
                self.redis,
                timeout_seconds=self.settings.redis_timeout_seconds,
            )

    async def start(self) -> None:
        await self.identity.hasher.warm_up()
        if self.settings.click_flusher_enabled:
            await self.analytics.flusher.start()

    async def close(self) -> None:
        await self.analytics.flusher.stop()
        await self.record_click.drain()
        await close_redis(self.redis)
        await self.database.dispose()


def build_services(settings: Settings) -> Services:
    bulkheads = build_bulkheads(settings)
    redis_breaker = CircuitBreaker(
        "redis",
        failure_threshold=settings.circuit_breaker_failure_threshold,
        recovery_timeout=settings.circuit_breaker_recovery_timeout_seconds,
        half_open_max_calls=settings.circuit_breaker_half_open_max_calls,
    )
    database_breaker = CircuitBreaker(
        "postgres",
        failure_threshold=settings.circuit_breaker_failure_threshold,
        recovery_timeout=settings.circuit_breaker_recovery_timeout_seconds,
        half_open_max_calls=settings.circuit_breaker_half_open_max_calls,
    )
    redis = create_redis(settings)
    database = Database(
        settings,
        breaker=database_breaker,
        read_bulkhead=bulkheads.get("db_read"),
        write_bulkhead=bulkheads.get("db_write"),
    )
    limiter = RateLimiter(
        redis=RedisTokenBucket(redis),
        policies=build_policies(settings),
        memory=MemoryTokenBucket(),
        breaker=redis_breaker,
        redis_timeout_seconds=settings.redis_timeout_seconds,
    )
    clock = SystemClock()
    resolver = SystemHostResolver(
        bulkhead=bulkheads.get("dns"),
        timeout_seconds=settings.dns_timeout_seconds,
    )
    url_policy = UrlPolicy(resolver=resolver, own_hosts=_own_hosts(settings))
    repository = SqlAlchemyLinkRepository(database)
    link_cache = RedisLinkCache(
        redis,
        breaker=redis_breaker,
        settings=settings,
    )
    quota = RedisDailyQuota(
        redis,
        breaker=redis_breaker,
        timeout_seconds=settings.redis_timeout_seconds,
    )
    publisher = RedisClickPublisher(
        redis,
        breaker=redis_breaker,
        settings=settings,
    )
    flusher = ClickFlusher(
        redis,
        database,
        breaker=redis_breaker,
        settings=settings,
    )
    stats_repository = SqlAlchemyStatsRepository(database)
    stats_cache = RedisStatsCache(
        redis,
        breaker=redis_breaker,
        settings=settings,
    )
    record_click = RecordClick(clock=clock, publisher=publisher)
    code_generator = CodeGenerator()

    users = SqlAlchemyUserRepository(database)
    sessions = SqlAlchemySessionRepository(database)
    hasher = Argon2PasswordHasher(
        bulkhead=bulkheads.get("hashing"),
        time_cost=settings.argon2_time_cost,
        memory_kib=settings.argon2_memory_kib,
        parallelism=settings.argon2_parallelism,
        hash_len=settings.argon2_hash_len,
        salt_len=settings.argon2_salt_len,
    )
    access_tokens = PyJwtAccessTokens(settings)
    throttle = RedisAuthThrottle(
        redis,
        limiter=limiter,
        breaker=redis_breaker,
        settings=settings,
    )
    google_oidc = GoogleOIDCClient(settings)
    session_issuer = SessionIssuer(
        access_tokens=access_tokens,
        sessions=sessions,
        clock=clock,
        refresh_ttl_days=settings.refresh_token_ttl_days,
    )
    identity = IdentityServices(
        users=users,
        sessions=sessions,
        hasher=hasher,
        access_tokens=access_tokens,
        throttle=throttle,
        google_oidc=google_oidc,
        clock=clock,
        register=Register(
            users=users,
            password_policy=PasswordPolicy(),
            hasher=hasher,
            throttle=throttle,
            clock=clock,
        ),
        login=Login(
            users=users,
            hasher=hasher,
            throttle=throttle,
            session_issuer=session_issuer,
        ),
        refresh_session=RefreshSession(
            users=users,
            sessions=sessions,
            access_tokens=access_tokens,
            clock=clock,
            refresh_ttl_days=settings.refresh_token_ttl_days,
        ),
        logout=Logout(sessions=sessions, clock=clock),
        get_me=GetMe(users=users),
        update_me=UpdateMe(users=users),
        get_avatar=GetAvatar(users=users),
        set_avatar=SetAvatar(users=users, clock=clock),
        remove_avatar=RemoveAvatar(users=users),
        google_login=LoginWithGoogle(
            users=users,
            session_issuer=session_issuer,
            clock=clock,
        ),
        authenticate_access=AuthenticateAccess(
            access_tokens=access_tokens,
            users=users,
        ),
    )

    links = LinkServices(
        repository=repository,
        cache=link_cache,
        url_policy=url_policy,
        code_generator=code_generator,
        clock=clock,
        quota=quota,
        create_link=CreateLink(
            repository=repository,
            cache=link_cache,
            url_policy=url_policy,
            code_generator=code_generator,
            quota=quota,
            clock=clock,
            anon_daily_limit=settings.anon_daily_link_limit,
            user_daily_limit=settings.user_daily_link_limit,
            anon_ttl_days=settings.anon_link_ttl_days,
        ),
        get_link=GetLink(repository=repository),
        get_overview=GetLinksOverview(repository=repository, clock=clock),
        list_links=ListLinks(repository=repository),
        update_link=UpdateLink(
            repository=repository,
            cache=link_cache,
            url_policy=url_policy,
            clock=clock,
        ),
        delete_link=DeleteLink(repository=repository, cache=link_cache),
        resolve_link=ResolveLink(repository=repository, cache=link_cache, clock=clock),
    )
    return Services(
        settings=settings,
        redis=redis,
        cache=CacheClient(
            redis,
            namespace="cache",
            breaker=redis_breaker,
            timeout_seconds=settings.redis_timeout_seconds,
        ),
        database=database,
        rate_limiter=limiter,
        redis_breaker=redis_breaker,
        database_breaker=database_breaker,
        bulkheads=bulkheads,
        links=links,
        identity=identity,
        analytics=AnalyticsServices(
            publisher=publisher,
            flusher=flusher,
            stats_repository=stats_repository,
            stats_cache=stats_cache,
            get_link_stats=GetLinkStats(
                links=repository,
                stats=stats_repository,
                cache=stats_cache,
                clock=clock,
            ),
        ),
        record_click=record_click,
    )


def _own_hosts(settings: Settings) -> set[str]:
    hosts: set[str] = set()
    for url in (settings.short_base_url, settings.frontend_origin, settings.api_public_base_url):
        try:
            host = urlsplit(url).hostname
        except ValueError:
            continue
        if host:
            hosts.add(host.lower())
    return hosts
