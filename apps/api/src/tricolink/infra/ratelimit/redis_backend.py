from __future__ import annotations

import math
from typing import Any, cast

from redis.asyncio import Redis

from tricolink.infra.ratelimit.models import RateLimitResult
from tricolink.infra.ratelimit.policies import BucketPolicy

TOKEN_BUCKET_LUA = """
local key = KEYS[1]
local capacity = tonumber(ARGV[1])
local refill = tonumber(ARGV[2])
local cost = tonumber(ARGV[3])
local ttl_ms = tonumber(ARGV[4])

local time_parts = redis.call('TIME')
local now_ms = tonumber(time_parts[1]) * 1000 + math.floor(tonumber(time_parts[2]) / 1000)

local stored = redis.call('HMGET', key, 'tokens', 'ts')
local tokens = tonumber(stored[1])
local last_ms = tonumber(stored[2])

if tokens == nil or last_ms == nil then
  tokens = capacity
  last_ms = now_ms
end

local elapsed_ms = now_ms - last_ms
if elapsed_ms < 0 then
  elapsed_ms = 0
end
tokens = math.min(capacity, tokens + (elapsed_ms / 1000.0) * refill)

local allowed = 0
local retry_after_ms = 0
if tokens >= cost then
  tokens = tokens - cost
  allowed = 1
else
  local missing = cost - tokens
  if refill > 0 then
    retry_after_ms = math.ceil((missing / refill) * 1000)
  else
    retry_after_ms = -1
  end
end

redis.call('HSET', key, 'tokens', tostring(tokens), 'ts', tostring(now_ms))
redis.call('PEXPIRE', key, ttl_ms)

return {allowed, math.floor(tokens), retry_after_ms}
"""


class RedisTokenBucket:
    """Atomic token bucket backed by a single Redis Lua script."""

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def consume(
        self,
        key: str,
        policy: BucketPolicy,
        cost: int = 1,
    ) -> RateLimitResult:
        raw = await self._redis.eval(
            TOKEN_BUCKET_LUA,
            1,
            key,
            policy.capacity,
            policy.refill_per_sec,
            cost,
            policy.ttl_ms,
        )
        values = cast(list[Any], raw)
        allowed = int(values[0]) == 1
        remaining = max(0, int(values[1]))
        retry_after_ms = int(values[2])

        if allowed:
            reset_after_seconds = _reset_seconds(policy, remaining)
        elif retry_after_ms >= 0:
            reset_after_seconds = max(1, math.ceil(retry_after_ms / 1000))
        else:
            reset_after_seconds = policy.seconds_to_fill

        return RateLimitResult(
            allowed=allowed,
            limit=policy.capacity,
            remaining=remaining,
            retry_after_ms=retry_after_ms,
            reset_after_seconds=reset_after_seconds,
        )


def _reset_seconds(policy: BucketPolicy, remaining: int) -> int:
    if policy.refill_per_sec <= 0:
        return -1
    return max(0, math.ceil((policy.capacity - remaining) / policy.refill_per_sec))
