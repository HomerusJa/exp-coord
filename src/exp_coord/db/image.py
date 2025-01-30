from datetime import datetime

from beanie import Document, Link

from exp_coord.db.device import Device


class Image(Document):
    """An image taken by a camera device."""

    device: Link[Device]
    taken_at: datetime

    # TODO: Add GridFS integration

    class Settings:
        name = "images"
        validate_on_save = True


# async def upload_image(image_model: Image, image_data: Any) -> BeanieObjectId:
#     """Upload an image to the database."""
#     filename = f"{image_model.device.s3i_id}_{image_model.taken_at}.jpg"
#
#     fs = get_grid_fs_client()
#     return await fs.upload_from_stream(
#         filename,
#         image_data,
#         metadata={
#             "device_s3i_id": image_model.device.s3i_id,
#             "taken_at": image_model.taken_at,
#         },
#     )
#
# async def download_image(image_model: Image) -> StreamTypeNotExistent: ...
