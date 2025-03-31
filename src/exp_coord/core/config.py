from pathlib import Path
from typing import Annotated, Any, Literal, cast

import toml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings

from exp_coord.services.s3i.base.annotations import (
    S3IEventQueueType,
    S3IIdType,
    S3IMessageQueueType,
)


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
    config_url: str

    topics: S3IEventTopics = Field(default_factory=S3IEventTopics)


class CollectionNames(BaseModel):
    all_messages_and_events: str = "all_messages_and_events"
    device: str = "devices"
    image: str = "images"
    image_gridfs: str = "image_files"
    status: str = "statuses"


class MongoDBSettingsBase(BaseModel):
    url: str
    db_name: str
    collection_names: CollectionNames = Field(default_factory=CollectionNames)


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


def _deep_update(destination_dict: dict[str, Any], update_dict: dict[str, Any]) -> dict[str, Any]:
    """Recursively update a dictionary."""
    for key, value in update_dict.items():
        if (
            isinstance(value, dict)
            and key in destination_dict
            and isinstance(destination_dict[key], dict)
        ):
            _deep_update(destination_dict[key], value)
        else:
            destination_dict[key] = value
    return destination_dict


def update_settings(
    override_values: dict[str, Any] | None = None, config_path: Path | None = None
) -> Settings:
    """Update global settings with new values or from a different config file.

    Args:
        override_values: Dictionary of values to override
        config_path: Alternative config file path

    Returns:
        Updated Settings instance
    """
    global __settings

    if config_path is None:
        config_path = find_file("config.toml")

    with open(config_path, "r") as f:
        config = toml.load(f)

    if override_values:
        _deep_update(config, override_values)

    # settings is global
    settings = Settings.model_validate(config)

    return settings


# Declare the settings variable with the proper type
# Using "typing.cast" to tell the type checker this will be initialized in the next line
__settings: Settings = cast(Settings, None)
update_settings()


def get_settings() -> Settings:
    global __settings
    if __settings is None:
        __settings = update_settings()
    return __settings
