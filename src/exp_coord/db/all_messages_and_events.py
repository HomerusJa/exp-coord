from datetime import datetime

from beanie import Document
from pydantic import Field

from exp_coord.services.s3i.models import S3IEvent, S3IMessageType


class AllMessagesAndEvents(Document):
    data: S3IMessageType | S3IEvent
    added_at: datetime = Field(default_factory=datetime.utcnow)
