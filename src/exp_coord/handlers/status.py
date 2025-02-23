"""Handling of status events."""

from loguru import logger

from exp_coord.core.config import settings
from exp_coord.db.device import get_device_by_s3i_id
from exp_coord.db.status import Status
from exp_coord.services.s3i import EventHandler, S3IEvent


def is_status_event(event: S3IEvent) -> bool:
    """Check if the event is a status event."""
    return event.topic == settings.s3i.topics.status


async def handle_status_event(event: S3IEvent) -> None:
    """Handle a status event."""
    device = get_device_by_s3i_id(event.sender)
    status = Status(
        device=device,
        status_name=event.content["status_name"],
        status_error_detail=event.content["status_error_detail"],
        status_error_source=event.content["status_error_source"],
        status_error_text=event.content["status_error_text"],
        sent_timestamp=event.timestamp,
    ).insert()
    logger.success(f"Status event saved: {status}")


status_handler = EventHandler(
    name="status",
    predicate=is_status_event,
    handle=handle_status_event,
)
