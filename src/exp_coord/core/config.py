from pathlib import Path
from typing import Annotated, Literal

import toml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings

from exp_coord.core.annotations.s3i import S3IEventQueueType, S3IIdType, S3IMessageQueueType

__all__ = ["Settings", "settings"]


def find_file(filename: str, base_path: Path | None = None) -> Path:
    """Find a file in the parent directories of base_path.

    Args:
        filename (str):
    """
    if base_path is None:
        base_path = Path(__file__).parent

    path: Path = base_path.resolve()
    while not path.is_mount() and not (path / filename).exists():
        path = path.parent
    if path.is_mount():
        raise FileNotFoundError(
            f"File '{filename}' not found in parent directories of '{base_path}'"
        )
    return path / filename


class S3IEventTopics(BaseModel):
    new_image: str = "plant-growth-observation_new-image"
    status: str = "plant-growth-observation_status"


class S3ISettings(BaseModel):
    client_id: S3IIdType
    client_secret: str
    message_queue: S3IMessageQueueType
    event_queue: S3IEventQueueType

    auth_url: str
    auth_realm: str
    broker_url: str

    topics: S3IEventTopics = Field(default_factory=S3IEventTopics)


class MongoDBSettingsBase(BaseModel):
    url: str
    db_name: str


class MongoDBSettingsPassword(MongoDBSettingsBase):
    connection_type: Annotated[Literal["password"], "password"]


class MongoDBSettingsX509(MongoDBSettingsBase):
    connection_type: Annotated[Literal["x509"], "x509"]
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
