import asyncio
from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, Sequence, TypeVar

from loguru import logger

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
        matching = [h for h in self._handlers if h.predicate(message)]

        if not matching:
            logger.warning(f"No handlers found for message: {message}")
        else:
            logger.debug(
                f"Found {len(matching)} handlers ({', '.join(map(str, matching))}) for message: {message}"
            )

        return matching

    async def process(self, message: T) -> None:
        """Process a message with all matching handlers.

        Raises:
            ExceptionGroup: If any error occurred during processing from one of the handlers.
        """
        handlers = self.find_handlers(message)

        exceptions: list[Exception] = []
        for handler in handlers:
            logger.debug(f"Handler {handler.name} started processing message: {message}")

            try:
                await handler.handle(message)
                logger.success(f"Handler {handler.name} successfully processed message: {message}")
            except Exception as exc:  # noqa: BLE001
                exceptions.append(exc)
                logger.exception(f"Handler {handler.name} failed to process message: {message}")
        if exceptions:
            raise ExceptionGroup(
                f"The message <{message}> (partially) failed to process", exceptions
            )

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
