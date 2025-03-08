import pytest
from beanie import init_beanie

from exp_coord.core.config import settings, update_settings
from exp_coord.db.connection import __models__, _create_client
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
async def _setup_database() -> None:
    db_name = settings.mongodb.db_name + "-test"
    update_settings({"mongodb": {"db_name": db_name}})
    client = _create_client()
    database = client[db_name]
    await init_beanie(database, document_models=__models__)

    # Create all the dummy data
    await create_dummy_devices()

    try:
        yield
    finally:
        # client.drop_database(database)
        client.close()
