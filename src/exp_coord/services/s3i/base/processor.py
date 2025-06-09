import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, Sequence, TypeVar

from structlog.stdlib import get_logger

logger = get_logger(__name__)
T = TypeVar("T")


@dataclass
class Handler(Generic[T]):
    """Generic handler that can process any type of message."""

    name: str
    predicate: Callable[[T], bool]
    handle: Callable[[T], Awaitable[None]]

    def __str__(self) -> str:
        return self.name


class Processor(Generic[T]):
    """Generic message processor that can handle any type of message."""

    def __init__(self, handlers: Sequence[Handler[T]]):
        """Initialize with handlers and optional custom logger."""
        self._handlers = handlers

    def find_handlers(self, message: T) -> list[Handler[T]]:
        """Find handlers that can process the message."""
        message_logger = logger.bind(content=message)
        matching = [h for h in self._handlers if h.predicate(message)]

        if not matching:
            message_logger.warning("No handlers found")
        else:
            message_logger.debug(
                f"Found {len(matching)} handlers ({', '.join(map(str, matching))})"
            )

        return matching

    async def process(self, message: T) -> None:
        """Process a message with all matching handlers.

        Raises:
            ExceptionGroup: If any error occurred during processing from one of the handlers.
        """
        message_logger = logger.bind(content=message)
        handlers = self.find_handlers(message)

        exceptions: list[Exception] = []
        for handler in handlers:
            message_logger.debug("Handler started processing", handler=handler.name)

            try:
                await handler.handle(message)
                message_logger.info("Handler finished successfully", handler=handler.name)
            except Exception as exc:
                exceptions.append(exc)
                message_logger.exception("Handler failed to process message", handler=handler.name)
        if exceptions:
            raise ExceptionGroup("The message (partially) failed to process", exceptions)

    async def process_all(self, messages: Sequence[T]) -> None:
        """Process all messages concurrently. This also merges all the ExceptionGroups into one."""
        tasks = (self.process(message) for message in messages)
        results: Sequence[None | BaseException] = await asyncio.gather(
            *tasks, return_exceptions=True
        )

        exceptions = []
        for result in results:
            if isinstance(result, ExceptionGroup):
                exceptions.extend(result.exceptions)  # Unpack nested exceptions
            elif isinstance(result, BaseException):
                exceptions.append(result)

        if exceptions:
            raise ExceptionGroup("Merged exceptions from process_all", exceptions)
