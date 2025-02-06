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

__client: AsyncIOMotorClient | None = None
__grid_fs_client: AsyncIOMotorGridFSBucket | None = None


def get_client() -> AsyncIOMotorClient:
    if not __client:
        raise RuntimeError("Database connection not established")
    return __client


def get_db() -> AsyncIOMotorDatabase:
    return get_client()[settings.mongodb.db_name]


def get_grid_fs_client() -> AsyncIOMotorGridFSBucket:
    if not __grid_fs_client:
        raise RuntimeError("GridFS connection not established")
    return __grid_fs_client


async def init_db() -> None:
    global __client
    global __grid_fs_client

    logger.info("Initializing database connection")
    __client = AsyncIOMotorClient(
        settings.mongodb.url,
        tls=True,
        tlsCertificateKeyFile=str(settings.mongodb.x509_cert_file),
    )

    logger.trace("Pinging the database to ensure the connection is successful")
    await get_client().admin.command("ping")
    logger.info("Database connection established")

    await init_beanie(get_db(), document_models=__models__)
    logger.info("Beanie initialized")

    logger.info("Initializing GridFS connection")
    __grid_fs_client = AsyncIOMotorGridFSBucket(get_db())
    logger.info("GridFS connection established")
