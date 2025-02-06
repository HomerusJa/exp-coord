from datetime import datetime

from beanie import Document, Link

from .device import Device


class Status(Document):
    """A status of a device at a certain time."""

    device: Link[Device]

    status_name: str
    status_error_detail: str
    status_error_source: str
    status_error_text: str

    # TODO: Consider converting this to a timeseries index
    sent_timestamp: datetime
    received_timestamp: datetime

    class Settings:
        name = "statuses"
        validate_on_save = True
