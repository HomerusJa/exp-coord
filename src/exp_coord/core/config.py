from pathlib import Path
from typing import Literal

import toml
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings

__all__ = ["Settings", "settings"]


def find_file(filename: str) -> Path:
    path: Path = Path(__file__).parent.resolve()
    while path != Path("/") and not (path / filename).exists():
        path = path.parent
    if path == Path("/"):
        raise FileNotFoundError(f"{filename} not found")
    return path / filename


class S3ISettings(BaseModel):
    auth_url: str
    auth_realm: str
    client_id: str
    client_secret: str
    broker_url: str


class MongoDBSettingsBase(BaseModel):
    connection_type: Literal["x509", "username"]
    url: str
    db_name: str


class MongoDBSettingsPassword(MongoDBSettingsBase):
    connection_type: Literal["password"]


class MongoDBSettingsX509(MongoDBSettingsBase):
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
