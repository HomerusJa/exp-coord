from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path
import toml

__all__ = ["settings", "Settings"]


def find_config_file() -> Path:
    path: Path = Path(__file__).parent.resolve()
    while path != Path("/") and not (path / "config.toml").exists():
        path = path.parent
    if path == Path("/"):
        raise FileNotFoundError("config.toml not found")
    return path / "config.toml"


class S3ISettings(BaseModel):
    auth_url: str
    auth_realm: str
    client_id: str
    client_secret: str
    broker_url: str


class MongoDBSettings(BaseModel):
    url: str
    db_name: str


class Settings(BaseSettings):
    s3i: S3ISettings
    mongodb: MongoDBSettings


def _get_settings():
    path = find_config_file()
    with open(path, "r") as f:
        config = toml.load(f)
    return Settings.model_validate(config)


settings = _get_settings()
