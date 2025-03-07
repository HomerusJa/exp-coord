import pytest

from exp_coord.core.config import update_settings
from exp_coord.db.connection import close_db, init_db


@pytest.fixture(scope="package", autouse=True)
async def setup_database():
    update_settings({"mongodb": {"db_name": "exp-coord-test"}})
    await init_db()

    try:
        yield
    finally:
        await close_db()
