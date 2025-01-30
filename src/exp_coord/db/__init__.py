from beanie import init_beanie, Document, UnionDoc, View
from motor.motor_asyncio import AsyncIOMotorClient

from loguru import logger

from exp_coord.core.config import settings

from exp_coord.db.device import Device
from exp_coord.db.image import Image
from exp_coord.db.status import Status

__models__: list[type[Document] | type[UnionDoc] | type[View]] = [
    Device,
    Image,
    Status,
]

__all__ = ["init_db", *__models__]


async def init_db() -> None:
    logger.info("Initializing database connection")
    client = AsyncIOMotorClient(
        settings.mongodb.url,
        tls=True,
        tlsCertificateKeyFile=str(settings.mongodb.x509_cert_file),
    )
    await init_beanie(client[settings.mongodb.db_name], document_models=__models__)
    logger.trace("Beanie initialized")

    # Ping the database to ensure the connection is successful
    await client.admin.command("ping")
    logger.success("Database connection established")
