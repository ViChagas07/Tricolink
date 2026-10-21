from __future__ import annotations

import asyncio
import secrets

from argon2 import PasswordHasher as Argon2Hasher
from argon2 import Type
from argon2.exceptions import Argon2Error

from tricolink.infra.resilience import Bulkhead


class Argon2PasswordHasher:
    """Argon2id hashing isolated behind the ``hashing`` bulkhead."""

    def __init__(
        self,
        *,
        bulkhead: Bulkhead,
        time_cost: int,
        memory_kib: int,
        parallelism: int,
        hash_len: int,
        salt_len: int,
    ) -> None:
        self._bulkhead = bulkhead
        self._hasher = Argon2Hasher(
            time_cost=time_cost,
            memory_cost=memory_kib,
            parallelism=parallelism,
            hash_len=hash_len,
            salt_len=salt_len,
            type=Type.ID,
        )
        self._dummy_hash: str | None = None
        self._dummy_lock = asyncio.Lock()

    async def hash(self, password: str) -> str:
        if not password or len(password) > 128:
            raise ValueError("password length is invalid")
        async with self._bulkhead.acquire():
            return await asyncio.to_thread(self._hasher.hash, password)

    async def verify(self, password: str, password_hash: str) -> bool:
        if not password or len(password) > 128 or not password_hash:
            return False
        async with self._bulkhead.acquire():
            try:
                return await asyncio.to_thread(
                    self._hasher.verify,
                    password_hash,
                    password,
                )
            except Argon2Error:
                return False

    async def warm_up(self) -> None:
        await self._get_dummy_hash()

    async def verify_dummy(self, password: str) -> None:
        dummy = await self._get_dummy_hash()
        await self.verify(password[:128], dummy)

    async def _get_dummy_hash(self) -> str:
        if self._dummy_hash is not None:
            return self._dummy_hash
        async with self._dummy_lock:
            if self._dummy_hash is None:
                self._dummy_hash = await self.hash(secrets.token_urlsafe(32))
            return self._dummy_hash
