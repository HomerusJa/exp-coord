from typing import AsyncGenerator

import pytest

from exp_coord.core.config import get_settings, update_settings
from exp_coord.db.connection import close_db, get_db, init_db
from exp_coord.db.device import Device


async def create_dummy_devices():
    SAMPLE_DEVICES_LIST = [
        {
            "s3i_id": "s3i:ab1b96cb-2181-41c6-8aaa-8ad61b813198",
            "rhizotron_num": None,
            "type": "coordinator",
            "s3i_msg_queue": "s3ibs://s3i:ab1b96cb-2181-41c6-8aaa-8ad61b813198",
            "s3i_ev_queue": "s3ib://s3i:ab1b96cb-2181-41c6-8aaa-8ad61b813198/event",
        },
        {
            "s3i_id": "s3i:eb13aa70-ede6-4f98-9eb9-fc7e2f91f1d3",
            "rhizotron_num": 1,
            "type": "camera",
            "s3i_msg_queue": "s3ibs://s3i:eb13aa70-ede6-4f98-9eb9-fc7e2f91f1d3",
            "s3i_ev_queue": None,
        },
        {
            "s3i_id": "s3i:4eadfd01-0eef-4567-ab01-0d6add9c9a0c",
            "rhizotron_num": 2,
            "type": "camera",
            "s3i_msg_queue": "s3ibs://s3i:4eadfd01-0eef-4567-ab01-0d6add9c9a0c",
            "s3i_ev_queue": None,
        },
    ]
    await Device.insert_many([Device.model_validate(entry) for entry in SAMPLE_DEVICES_LIST])


@pytest.fixture(scope="session", name="setup_database")
async def _setup_database() -> AsyncGenerator[None, None]:
    db_name = get_settings().mongodb.db_name + "-test"
    update_settings({"mongodb": {"db_name": db_name}})

    await init_db()
    assert get_db().name == db_name, (
        f"The db name was not updated properly, {get_db().name=}, not {db_name=}"
    )  # FIXME

    # Create all the dummy data
    await create_dummy_devices()

    try:
        yield
    finally:
        # client.drop_database(database)
        await close_db()
