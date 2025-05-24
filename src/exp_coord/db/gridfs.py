import datetime
from typing import Any

import pydantic
from beanie import PydanticObjectId
from bson import ObjectId
from pydantic import BaseModel, Field, model_validator

from exp_coord.db.connection import create_grid_fs_client


class GridFSFileMetadata(BaseModel):
    """Metadata for a file stored in GridFS."""

    from_collection: str | None = None
    from_id: PydanticObjectId | None = None
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

    # Use Field with annotation to preserve parent's type signatures
    from_collection: str | None = Field(default="images")

    # Again, we need to keep the type signature of the parent class. In the validator below,
    # we ensure that from_id is set.
    # FIXME: This is not ideal, as it destroys the type annotations.
    from_id: PydanticObjectId | None = Field(default=None)

    @model_validator(mode="after")
    def ensure_values_are_set(self):
        if self.from_collection != "images":
            raise ValueError(f"from_collection must be 'images', not {self.from_collection}")

        if self.from_id is None:
            raise ValueError("from_id must be set")

        return self


@pydantic.validate_call(config=pydantic.ConfigDict(arbitrary_types_allowed=True))
async def upload_to_gridfs(
    filename: str,
    file_data: Any,
    metadata: GridFSFileMetadata,
    bucket_name: str = "fs",
) -> ObjectId:
    """Upload a file to GridFS. file_data should be a stream supported by Motor."""
    fs = create_grid_fs_client(bucket_name=bucket_name)
    return await fs.upload_from_stream(filename, file_data, metadata=metadata.dict())
