from datetime import datetime

from beanie import Document
from pydantic import Field

from exp_coord.core.config import get_settings
from exp_coord.services.s3i.broker.models import S3IEvent, S3IMessage


class AllMessagesAndEvents(Document):
    data: S3IMessage | S3IEvent
    added_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = get_settings().mongodb.collection_names.all_messages_and_events
        validate_on_save = True
