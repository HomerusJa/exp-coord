from datetime import datetime

from beanie import Document, Link

from .device import Device


class Image(Document):
    """An image taken by a camera device."""

    device: Link[Device]

    # TODO: Add file storage in GridFS in the future

    taken_at: datetime

    class Settings:
        name = "images"
