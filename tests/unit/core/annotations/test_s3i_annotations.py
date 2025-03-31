import pytest
from pydantic import TypeAdapter

from exp_coord.services.s3i.base.annotations import (
    S3IQueueType,
    _validate_s3i_event_queue,
    _validate_s3i_id,
    _validate_s3i_message_queue,
)

VALID_IDS = [
    "s3i:ab1b96cb-2181-41c6-8aaa-8ad61b813198",
    "s3i:eb13aa70-ede6-4f98-9eb9-fc7e2f91f1d3",
    "s3i:4eadfd01-0eef-4567-ab01-0d6add9c9a0c",
]


VALID_MSG_QUEUES = [
    "s3ibs://s3i:ab1b96cb-2181-41c6-8aaa-8ad61b813198",
    "s3ibs://s3i:eb13aa70-ede6-4f98-9eb9-fc7e2f91f1d3",
    "s3ibs://s3i:4eadfd01-0eef-4567-ab01-0d6add9c9a0c",
]


VALID_EV_QUEUES = [
    "s3ib://s3i:ab1b96cb-2181-41c6-8aaa-8ad61b813198/event",
]


VALID_QUEUES = [*VALID_MSG_QUEUES, *VALID_EV_QUEUES]

INVALID_IDS = [
    "",
    "ab1b96cb-2181-41c6-8aaa-8ad61b813198",
    "s3i:abc",
    "s3i:ZZZZ-ZZZZ-ZZZZ-ZZZZ-ZZZZZZZZZZZZ",
]

INVALID_MSG_QUEUES = [*VALID_EV_QUEUES, "", "s3ibs://s3i:abc"]

INVALID_EV_QUEUES = [
    *VALID_MSG_QUEUES,
    "s3ib://s3i:ab1b96cb-2181-41c6-8aaa-8ad61b813198/events",  # It should be "/event", without the "s"
    "",
    "s3ib://s3i:abc/event",
]


@pytest.mark.parametrize("id", VALID_IDS)
def test_s3i_id_valid(id):
    assert _validate_s3i_id(id)


@pytest.mark.parametrize("id", INVALID_IDS)
def test_s3i_id_invalid(id):
    with pytest.raises(ValueError):
        _validate_s3i_id(id)


@pytest.mark.parametrize("queue", VALID_MSG_QUEUES)
def test_s3i_message_queue_valid(queue):
    assert _validate_s3i_message_queue(queue)


@pytest.mark.parametrize("queue", INVALID_MSG_QUEUES)
def test_s3i_message_queue_invalid(queue):
    with pytest.raises(ValueError):
        _validate_s3i_message_queue(queue)


@pytest.mark.parametrize("queue", VALID_EV_QUEUES)
def test_s3i_event_queue_valid(queue):
    assert _validate_s3i_event_queue(queue)


@pytest.mark.parametrize("queue", INVALID_EV_QUEUES)
def test_s3i_event_queue_invalid(queue):
    with pytest.raises(ValueError):
        _validate_s3i_event_queue(queue)


@pytest.fixture(scope="module")
def s3i_queue_ta() -> TypeAdapter[S3IQueueType]:
    return TypeAdapter[S3IQueueType](S3IQueueType)


@pytest.mark.parametrize("queue", VALID_QUEUES)
def test_s3i_queue_valid(s3i_queue_ta, queue):
    assert s3i_queue_ta.validate_python(queue)
