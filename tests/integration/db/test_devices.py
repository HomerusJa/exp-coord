from loguru import logger

from exp_coord.db.device import Device


async def test_with_sample_devices(setup_database):
    logger.debug(await Device.find_all().to_list())
