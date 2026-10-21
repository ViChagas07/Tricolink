import pytest
from sqlalchemy import text

from tricolink.core.config import Settings
from tricolink.infra.db import Database

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_database_ping_and_unit_of_work() -> None:
    database = Database(Settings.from_env())
    try:
        await database.ping()
        async with database.unit_of_work() as session:
            value = (await session.execute(text("SELECT 1"))).scalar_one()
        assert value == 1
    finally:
        await database.dispose()


@pytest.mark.asyncio
async def test_unit_of_work_rolls_back_on_error() -> None:
    database = Database(Settings.from_env())
    try:
        with pytest.raises(RuntimeError):
            async with database.unit_of_work() as session:
                await session.execute(text("SELECT 1"))
                raise RuntimeError("boom")
    finally:
        await database.dispose()
