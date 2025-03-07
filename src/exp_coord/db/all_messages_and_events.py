from datetime import datetime

from beanie import Document
from pydantic import Field

from exp_coord.core.config import settings
from exp_coord.services.s3i.models import S3IEvent, S3IMessageType


class AllMessagesAndEvents(Document):
    data: S3IMessageType | S3IEvent
    added_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = settings.mongodb.collection_names.all_messages_and_events
        validate_on_save = True
