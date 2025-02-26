"""A handler to just save every message and event to MongoDB."""

from exp_coord.db.all_messages_and_events import AllMessagesAndEvents
from exp_coord.services.s3i import EventHandler, MessageHandler, S3IEvent, S3IMessageType


async def save_event_or_message(event: S3IEvent | S3IMessageType) -> None:
    """Save the event to MongoDB."""
    await AllMessagesAndEvents(data=event).insert()


SaveAllEventsHandler = EventHandler(
    name="save_all",
    predicate=lambda event: True,
    handle=save_event_or_message,
)

SaveAllMessagesHandler = MessageHandler(
    name="save_all",
    predicate=lambda message: True,
    handle=save_event_or_message,
)
