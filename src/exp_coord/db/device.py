from typing import Literal

from beanie import Document
from pydantic import model_validator

from exp_coord.core.annotations.s3i import S3IEventQueueType, S3IIdType, S3IMessageQueueType


class Device(Document):
    """A device participating in an experiment."""

    name: str | None = None
    s3i_id: S3IIdType
    rhizotron_num: int | None = None
    type: Literal["camera", "water_supply", "coordinator"]

    s3i_msg_queue: S3IMessageQueueType | None = None
    s3i_ev_queue: S3IEventQueueType | None = None

    @model_validator(mode="after")
    def set_default_name(self):
        if self.name is None:
            self.name = f"{self.type}_at_{self.rhizotron_num}-{self.s3i_id}"

        return self

    class Settings:
        name = "devices"
        validate_on_save = True
