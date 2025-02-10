import asyncio

import typer
from loguru import logger

from exp_coord.core.config import settings
from exp_coord.core.log import setup_logging
from exp_coord.db.connection import init_db
from exp_coord.services.s3i import S3IBrokerClient

app = typer.Typer(name="exp_coord")


@app.callback()
def startup() -> None:
    logger.debug(f"Using following settings: {settings}")
    setup_logging()
    asyncio.run(init_db())


async def async_run() -> None:
    async with S3IBrokerClient() as client:
        print(await client.get_message())
        print(await client.get_event())


@app.command()
def run() -> None:
    logger.info("Running once")
    asyncio.run(async_run())


@app.command()
def run_forever() -> None:
    logger.info("Running forever")
