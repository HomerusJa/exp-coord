"""Implements the handler for a new image event."""

from datetime import datetime
from typing import Literal

from beanie import PydanticObjectId
from pydantic import Base64UrlBytes, BaseModel, Field, computed_field

from exp_coord.core.config import get_settings
from exp_coord.db.device import get_device_by_s3i_id
from exp_coord.db.gridfs import ImageFileMetadata, upload_to_gridfs
from exp_coord.db.image import Image
from exp_coord.services.s3i import EventHandler, S3IEvent


def is_new_image_event(event: S3IEvent) -> bool:
    """Check if the event is a new image event."""
    return event.topic == get_settings().s3i.topics.new_image


class NewImageEventContent(BaseModel):
    """The content of a new image event."""

    type: Literal["image/jpeg; encoding=base64url"]
    path: str
    taken_at: int = Field(alias="takenAt")
    image: Base64UrlBytes = Field(repr=False)

    @computed_field
    def taken_at_datetime(self) -> datetime:
        """Convert the taken_at timestamp to a datetime."""
        return datetime.fromtimestamp(self.taken_at)


async def handle_new_image_event(event: S3IEvent) -> None:
    """Handle a new image event.

    For that, we need to:
    - Validate the event content.
    - Save the image data to GridFS.
    - Get the device that sent the event to later include it in the image record.
    - Create a new image record in the database.
    """
    content = NewImageEventContent.model_validate(event.content)
    device = await get_device_by_s3i_id(event.sender)
    image = Image(
        device=device,  # pyright: ignore[reportArgumentType]
        taken_at=datetime.fromtimestamp(content.taken_at),
        file_id=None,
    )
    await image.insert()
    assert image.id is not None, "Image ID is set after insertion."
    filename = await image.get_filename()
    metadata = ImageFileMetadata(from_id=image.id)
    file_id = await upload_to_gridfs(
        filename,
        content.image,
        metadata,
        bucket_name=get_settings().mongodb.collection_names.image_gridfs,
    )
    image.file_id = PydanticObjectId(file_id)
    await image.save()


NewImageHandler = EventHandler(
    name="new_image",
    predicate=is_new_image_event,
    handle=handle_new_image_event,
)
