import datetime
from typing import Any, Literal

from beanie import BeanieObjectId
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from pydantic import BaseModel, model_validator

from exp_coord.db.connection import get_grid_fs_client


class GridFSFileMetadata(BaseModel):
    """Metadata for a file stored in GridFS."""

    from_collection: str | None = None
    from_id: BeanieObjectId | None = None
    added_at: datetime.datetime | None = None
    last_modified_at: datetime.datetime | None = None

    @model_validator(mode="after")
    def set_default_timestamps(self):
        if self.added_at is None:
            self.added_at = datetime.datetime.now()

        if self.last_modified_at is None:
            self.last_modified_at = self.added_at

        return self

    class Config:
        json_encoders = {datetime.datetime: lambda dt: dt.isoformat()}  # noqa: RUF012


class ImageFileMetadata(GridFSFileMetadata):
    """Metadata for an image stored in GridFS."""

    from_collection: Literal["images"] = "images"
    from_id: BeanieObjectId  # Required


async def upload_to_gridfs(
    filename: str,
    file_data: Any,
    metadata: GridFSFileMetadata,
    fs: AsyncIOMotorGridFSBucket | None = None,
):
    """Upload a file to GridFS. file_data should be a stream supported by Motor."""
    if fs is None:
        fs = get_grid_fs_client()

    return await fs.upload_from_stream(filename, file_data, metadata=metadata.dict())
