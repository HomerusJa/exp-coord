from pathlib import Path
from typing import Literal

import toml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings

from .annotations.s3i import S3IEventQueueType, S3IIdType, S3IMessageQueueType

__all__ = ["Settings", "settings"]


def find_file(filename: str) -> Path:
    path: Path = Path(__file__).parent.resolve()
    while path != Path("/") and not (path / filename).exists():
        path = path.parent
    if path == Path("/"):
        raise FileNotFoundError(f"{filename} not found")
    return path / filename


class S3ISettings(BaseModel):
    client_id: S3IIdType
    client_secret: str
    message_queue: S3IMessageQueueType
    event_queue: S3IEventQueueType

    auth_url: str
    auth_realm: str
    broker_url: str


class MongoDBSettingsBase(BaseModel):
    connection_type: Literal["x509", "username"]
    url: str
    db_name: str


class MongoDBSettingsPassword(MongoDBSettingsBase):
    connection_type: Literal["password"]


class MongoDBSettingsX509(MongoDBSettingsBase):
    connection_type: Literal["x509"]
    x509_cert_file: Path

    @field_validator("x509_cert_file", mode="after")
    def validate_x509_cert_filename(cls, v):
        return find_file(v)


class Settings(BaseSettings):
    s3i: S3ISettings
    mongodb: MongoDBSettingsPassword | MongoDBSettingsX509 = Field(discriminator="connection_type")


def _get_settings():
    path = find_file("config.toml")
    with open(path, "r") as f:
        config = toml.load(f)
    return Settings.model_validate(config)


settings = _get_settings()
