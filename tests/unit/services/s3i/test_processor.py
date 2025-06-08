from unittest.mock import AsyncMock

import pytest

from exp_coord.services.s3i import Handler, Processor


def test_find_handlers():
    async def handle(message):
        pass

    handlers = [
        Handler("test1", lambda m: m == "test1", handle),
        Handler("test2", lambda m: m == "test2", handle),
    ]
    processor = Processor[str](handlers)

    assert processor.find_handlers("test1") == [handlers[0]]
    assert processor.find_handlers("test2") == [handlers[1]]
    assert processor.find_handlers("test3") == []


async def test_process():
    handle_1 = AsyncMock()
    handle_2 = AsyncMock()

    handlers = [
        Handler("test1", lambda m: m == "test1", handle_1),
        Handler("test2", lambda m: m == "test2", handle_2),
    ]
    processor = Processor[str](handlers)

    await processor.process("test1")
    handle_1.assert_awaited_once_with("test1")
    handle_2.assert_not_awaited()

    await processor.process("test1")
    handle_1.assert_awaited_with("test1")
    handle_2.assert_not_awaited()

    await processor.process("test2")
    handle_1.assert_awaited_with("test1")
    handle_2.assert_awaited_once_with("test2")


def test_logs(log_output):
    async def handle(message):
        pass

    handlers = [
        Handler("test1_handler1", lambda m: m == "test1", handle),
        Handler("test1_handler2", lambda m: m == "test1", handle),
    ]
    processor = Processor[str](handlers)

    assert processor.find_handlers("test1") == handlers
    assert any(
        entry["event"] == "Found 2 handlers (test1_handler1, test1_handler2) for message: test1"
        for entry in log_output.entries
    )
    assert processor.find_handlers("test2") == []
    assert any(
        entry["event"] == "No handlers found for message: test2" for entry in log_output.entries
    )


async def test_all_handlers_processed_even_if_one_failed():
    handle_1 = AsyncMock()
    handle_2 = AsyncMock()

    # First handler will raise an exception
    handle_1.side_effect = ValueError("Test error")

    # Second handler will be a normal mock
    handle_2.return_value = None

    handlers = [
        Handler("test1_handler1", lambda m: m == "test1", handle_1),
        Handler("test2_handler2", lambda m: m == "test1", handle_2),
    ]
    processor = Processor[str](handlers)

    # Expect an ExceptionGroup to be raised
    with pytest.raises(ExceptionGroup) as exc_info:
        await processor.process("test1")

    # Verify both handlers were called
    handle_1.assert_awaited_once_with("test1")
    handle_2.assert_awaited_once_with("test1")

    # Verify the ExceptionGroup contains the expected exception
    assert len(exc_info.value.exceptions) == 1
    assert isinstance(exc_info.value.exceptions[0], ValueError)
    assert str(exc_info.value.exceptions[0]) == "Test error"
