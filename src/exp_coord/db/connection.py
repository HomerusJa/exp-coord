from beanie import init_beanie
from loguru import logger
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
    AsyncIOMotorGridFSBucket,
)

from exp_coord.core.config import settings

__models__: list[str] = [
    "exp_coord.db.device.Device",
    "exp_coord.db.image.Image",
    "exp_coord.db.status.Status",
]

__all__ = [
    "get_client",
    "get_db",
    "get_grid_fs_client",
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
    return get_client()[settings.mongodb.db_name]


def get_grid_fs_client() -> AsyncIOMotorGridFSBucket:
    """Get the GridFS client, raising a RuntimeError if it is not initialized."""
    if not __grid_fs_client:
        raise RuntimeError("GridFS connection not established")
    return __grid_fs_client


def _create_client() -> AsyncIOMotorClient:
    """Create a new database client based on the connection type."""
    if settings.mongodb.connection_type == "password":
        logger.debug("Creating a new database client with password authentication")
        return AsyncIOMotorClient(settings.mongodb.url)
    elif settings.mongodb.connection_type == "x509":
        logger.debug("Creating a new database client with X.509 certificate authentication")
        return AsyncIOMotorClient(
            settings.mongodb.url,
            tls=True,
            tlsCertificateKeyFile=str(settings.mongodb.x509_cert_file),
        )
    else:
        raise ValueError(f"Invalid connection type: {settings.mongodb.connection_type}")


async def init_db() -> None:
    """Initialize the database, GridFS connection and beanie.

    You can run this function in a synchronous context using asyncio.run(init_db()).
    """
    global __client
    global __grid_fs_client

    logger.info("Initializing database connection")
    __client = _create_client()

    logger.trace("Pinging the database to ensure the connection is successful")
    await get_client().admin.command("ping")
    logger.info("Database connection established")

    await init_beanie(get_db(), document_models=__models__)
    logger.info("Beanie initialized")

    logger.info("Initializing GridFS connection")
    __grid_fs_client = AsyncIOMotorGridFSBucket(get_db())
    logger.info("GridFS connection established")
