from dataclasses import dataclass
from typing import Awaitable, Callable, Generic, Sequence, TypeAlias, TypeVar

from loguru import logger

from exp_coord.services.s3i import S3IEvent
from exp_coord.services.s3i.models import S3IMessageType

T = TypeVar("T")


@dataclass
class Handler(Generic[T]):
    """Generic handler that can process any type of message."""

    name: str
    predicate: Callable[[T], bool]
    handle: Callable[[T], Awaitable[None]]


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
        elif len(matching) > 1:
            logger.warning(
                f"Multiple handlers found for message: {message}. "
                f"Handlers: {', '.join(h.name for h in matching)}"
            )

        return matching

    async def process(self, message: T) -> None:
        """Process a message with all matching handlers."""
        handlers = self.find_handlers(message)

        for handler in handlers:
            logger.debug(f"Handler {handler.name} processing message: {message}")

            with logger.catch(
                level="ERROR",
                message=f"Handler {handler.name} failed to process message: {message}",
            ):
                await handler.handle(message)
                logger.success(f"Handler {handler.name} successfully processed message: {message}")


EventHandler: TypeAlias = Handler[S3IEvent]
EventProcessor: TypeAlias = Processor[S3IEvent]

MessageHandler: TypeAlias = Handler[S3IMessageType]
MessageProcessor: TypeAlias = Processor[S3IMessageType]
