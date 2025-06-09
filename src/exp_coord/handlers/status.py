"""Handling of status events."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel
from structlog.stdlib import get_logger

from exp_coord.core.config import get_settings
from exp_coord.db.device import get_device_by_s3i_id
from exp_coord.db.status import Status
from exp_coord.services.s3i import EventHandler, S3IEvent

logger = get_logger(__name__)


def is_status_event(event: S3IEvent) -> bool:
    """Check if the event is a status event."""
    return event.topic == get_settings().s3i.topics.status


class StatusEventContent(BaseModel):
    """Content of a status event."""

    type: Literal["status"] = "status"
    status: str
    detail: str = ""
    status_error_detail: str = ""
    status_error_source: str = ""
    status_error_text: str = ""


async def handle_status_event(event: S3IEvent) -> None:
    """Handle a status event."""
    content = StatusEventContent.model_validate(event.content)
    device = await get_device_by_s3i_id(event.sender)
    status = Status(
        device=device,  # pyright: ignore[reportArgumentType]
        status=content.status,
        status_error_detail=content.status_error_detail,
        status_error_source=content.status_error_source,
        status_error_text=content.status_error_text,
        sent_timestamp=datetime.fromtimestamp(event.timestamp),
    )
    await status.insert()
    logger.info("Status event saved", event=status)


StatusHandler = EventHandler(
    name="status",
    predicate=is_status_event,
    handle=handle_status_event,
)
