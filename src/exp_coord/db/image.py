from datetime import datetime

from beanie import Document, Link, PydanticObjectId

from exp_coord.db.device import Device


class Image(Document):
    """An image taken by a camera device. The images themselves should be stored in GridFS using the method below.

    Storage in GridFS has to be done manually. Consider the following example:
    ```python
    from exp_coord.db.image import Image
    from exp_coord.db.gridfs import ImageFileMetadata, upload_to_gridfs

    filename = await image.get_filename()
    image = Image(device=..., taken_at=..., filename=filename)
    metadata = ImageFileMetadata(from_id=image.id)
    with aiofiles.open("path/to/image.jpg", "rb") as f:
        file_id = upload_to_gridfs(filename, f, metadata)
        image.file_id = file_id
        await image.insert()
    ```
    """

    device: Link[Device] | Device
    taken_at: datetime

    file_id: PydanticObjectId | None = None

    async def get_filename(self) -> str:
        """Compute the filename of the image. This method has to be async because it fetches the device link."""
        await self.fetch_link("device")
        # self.device is getting cast to a Device object by the fetch_link method
        assert isinstance(self.device, Device), (
            "Device link should be fetched. This should never happen."
        )
        return f"{self.device.s3i_id}-{self.taken_at.isoformat()}.jpg"

    class Settings:
        name = "images"
        validate_on_save = True
