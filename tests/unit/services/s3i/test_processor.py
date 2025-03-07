from unittest.mock import AsyncMock

from logot import Logot, logged

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


def test_logs(logot: Logot):
    async def handle(message):
        pass

    handlers = [
        Handler("test1_handler1", lambda m: m == "test1", handle),
        Handler("test1_handler2", lambda m: m == "test1", handle),
    ]
    processor = Processor[str](handlers)

    assert processor.find_handlers("test1") == handlers
    logot.assert_logged(
        logged.warning(
            "Multiple handlers found for message: test1. Handlers: test1_handler1, test1_handler2"
        )
    )
    assert processor.find_handlers("test2") == []
    logot.assert_logged(logged.warning("No handlers found for message: test2"))


async def test_exception_logs(logot: Logot):
    async def handle(message):
        raise ValueError("Test error")

    handlers = [Handler("test1", lambda m: True, handle)]
    processor = Processor[str](handlers)

    # Exception is logged, not propagated
    await processor.process("some-message")

    logot.assert_logged(logged.error("Handler test1 failed to process message: some-message"))
