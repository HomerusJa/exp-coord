from typing import Annotated
from uuid import UUID

from pydantic import AfterValidator


def _validate_s3i_id(s3i_id: str) -> str:
    """Validate an S3I ID.

    An example of a valid S3I ID is 's3i:123e4567-e89b-12d3-a456-426614174000'.

    Raises:
        ValueError: If the S3I ID is not valid.
    """
    if not s3i_id.startswith("s3i:"):
        raise ValueError("S3I ID must start with 's3i:'")

    try:
        UUID(s3i_id[4:])
    except ValueError as exc:
        raise ValueError("S3I ID must end with a valid UUID") from exc

    return s3i_id


def _validate_s3i_message_queue(queue: str) -> str:
    """Validate an S3I message queue name.

    Raises:
        ValueError: If the queue name is not valid.
    """
    if not queue.startswith("s3ibs://"):
        raise ValueError("S3I queue name must start with 's3ibs://'")

    try:
        _validate_s3i_id(queue[8:])
    except ValueError as exc:
        raise ValueError("S3I queue name must end with a valid S3I ID") from exc

    return queue


def _validate_s3i_event_queue(queue: str) -> str:
    """Validate an S3I event queue name.

    Raises:
        ValueError: If the queue name is not valid.
    """
    if not queue.startswith("s3ib://"):
        raise ValueError("S3I queue name must start with 's3ib://'")
    if not queue.endswith("/event"):
        raise ValueError("S3I queue name must end with '/event'")

    try:
        _validate_s3i_id(queue[7:-6])
    except ValueError as exc:
        raise ValueError("S3I queue name must contain a valid S3I ID") from exc

    return queue


S3IIdType = Annotated[str, AfterValidator(_validate_s3i_id)]
S3IMessageQueueType = Annotated[str, AfterValidator(_validate_s3i_message_queue)]
S3IEventQueueType = Annotated[str, AfterValidator(_validate_s3i_event_queue)]
S3IQueueType = S3IMessageQueueType | S3IEventQueueType
