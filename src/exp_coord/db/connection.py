import asyncio

from beanie import init_beanie
from loguru import logger
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorGridFSBucket,
)

from exp_coord.core.config import get_settings
from exp_coord.db.all_messages_and_events import AllMessagesAndEvents
from exp_coord.db.device import Device
from exp_coord.db.image import Image
from exp_coord.db.status import Status

__models__ = [
    AllMessagesAndEvents,
    Device,
    Image,
    Status,
]

__all__ = [
    "create_grid_fs_client",
    "get_client",
    "get_db",
    "init_db",
]

__client: AsyncIOMotorClient | None = None
__grid_fs_client: AsyncIOMotorGridFSBucket | None = None


def get_client() -> AsyncIOMotorClient:
    """Get the database client, raising a RuntimeError if it is not initialized."""
    if not __client:
        raise RuntimeError("Database connection not established")
    return __client


def get_db() -> AsyncIOMotorDatabase:
    """Get the database, raising a RuntimeError if the client is not initialized."""
    logger.debug(f"{get_settings()=}")
    return get_client()[get_settings().mongodb.db_name]


def create_grid_fs_client(bucket_name: str = "fs") -> AsyncIOMotorGridFSBucket:
    """Create a new GridFS bucket."""
    return AsyncIOMotorGridFSBucket(get_db(), bucket_name=bucket_name)


def _create_client() -> AsyncIOMotorClient:
    """Create a new database client based on the connection type."""
    settings = get_settings()
    if settings.mongodb.connection_type == "password":
        logger.debug("Creating a new database client with password authentication")
        client = AsyncIOMotorClient(settings.mongodb.url)
    elif settings.mongodb.connection_type == "x509":
        logger.debug("Creating a new database client with X.509 certificate authentication")
        client = AsyncIOMotorClient(
            settings.mongodb.url,
            tls=True,
            tlsCertificateKeyFile=str(settings.mongodb.x509_cert_file),
        )
    else:
        raise ValueError(f"Invalid connection type: {settings.mongodb.connection_type}")

    # Reference: https://stackoverflow.com/a/69065287/22478603
    client.get_io_loop = asyncio.get_running_loop
    return client


async def init_db() -> None:
    """Initialize the database, GridFS connection and beanie.

    You can run this function in a synchronous context using asyncio.run(init_db()).
    """
    global __client
    global __grid_fs_client

    logger.debug(
        f"Initializing database connection at {get_settings().mongodb.url} using the database {get_settings().mongodb.db_name}"
    )
    __client = _create_client()

    logger.trace("Pinging the database to ensure the connection is successful")
    await get_client().admin.command("ping")
    logger.success("Database connection established")

    await init_beanie(get_db(), document_models=__models__)
    logger.success("Beanie initialized")


async def close_db() -> None:
    """Close the database connection properly."""
    logger.debug("Closing database connection")

    global __client

    if __client is None:
        logger.trace("Database connection already closed")
        return

    __client.close()
    __client = None
    logger.success("Database connection closed")
