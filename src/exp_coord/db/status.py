from datetime import datetime

from beanie import Document, Link
from pydantic import Field

from exp_coord.core.config import get_settings
from exp_coord.db.device import Device


class Status(Document):
    """A status of a device at a certain time."""

    device: Link[Device] | Device

    status_name: str
    status_error_detail: str = Field(default="")
    status_error_source: str = Field(default="")
    status_error_text: str = Field(default="")

    # TODO: Consider converting this to a timeseries index
    sent_timestamp: datetime
    received_timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = get_settings().mongodb.collection_names.status
        validate_on_save = True
