import pytest

from tricolink.core.config import Settings
from tricolink.infra.db import Database


class _FakeConnection:
    def __init__(self, migrated: bool) -> None:
        self._migrated = migrated

    async def __aenter__(self) -> "_FakeConnection":
        return self

    async def __aexit__(self, *args: object) -> None:
        return None

    async def scalar(self, statement: object) -> bool:
        return self._migrated


class _FakeEngine:
    def __init__(self, migrated: bool) -> None:
        self._migrated = migrated

    def connect(self) -> _FakeConnection:
        return _FakeConnection(self._migrated)


def _database_with_schema(migrated: bool) -> Database:
    database = Database.__new__(Database)
    database._settings = Settings.from_env()
    database._engine = _FakeEngine(migrated)
    database._read_bulkhead = None
    database._breaker = None
    return database


async def test_check_ready_accepts_migrated_schema() -> None:
    await _database_with_schema(True).check_ready()


async def test_check_ready_rejects_missing_schema() -> None:
    with pytest.raises(RuntimeError, match="not migrated"):
        await _database_with_schema(False).check_ready()
