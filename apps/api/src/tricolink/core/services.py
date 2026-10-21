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
from tricolink.modules.analytics.adapters import ClickFlusher, RedisClickPublisher
from tricolink.modules.links.adapters import RedisLinkCache, SqlAlchemyLinkRepository
from tricolink.modules.links.application import (
    CreateLink,
    DeleteLink,
    GetLink,
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
    list_links: ListLinks
    update_link: UpdateLink
    delete_link: DeleteLink
    resolve_link: ResolveLink


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
    analytics: AnalyticsServices
    record_click: RecordClick

    async def redis_ping(self) -> None:
        async with self.redis_breaker.guard():
            await ping_redis(
                self.redis,
                timeout_seconds=self.settings.redis_timeout_seconds,
            )

    async def start(self) -> None:
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
    record_click = RecordClick(clock=clock, publisher=publisher)
    code_generator = CodeGenerator()

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
        analytics=AnalyticsServices(publisher=publisher, flusher=flusher),
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
