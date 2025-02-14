"""Defines a class processing new S3I messages based on previously defined handlers."""

import asyncio
from typing import Protocol, overload, runtime_checkable

from loguru import logger

from exp_coord.services.s3i.models import S3IEvent, S3IMessageType


@runtime_checkable
class MessageHandler(Protocol):
    """Protocol for S3I message handlers."""

    @property
    def name(self) -> str:
        """Name of the handler."""
        ...

    def is_suited(self, message: S3IMessageType) -> bool:
        """Check if the handler is suited for the given message.

        Args:
            message (S3IMessageType): S3I message to check.

        Returns:
            bool: True if the handler is suited, False otherwise.
        """
        ...

    async def handle(self, message: S3IMessageType) -> None:
        """Handle an incoming S3I message.

        Args:
            message (S3IMessageType): S3I message to handle.
        """
        ...


@runtime_checkable
class EventHandler(Protocol):
    """Protocol for S3I event handlers."""

    @property
    def name(self) -> str:
        """Name of the handler."""
        ...

    def is_suited(self, event: S3IEvent) -> bool:
        """Check if the handler is suited for the given event.

        Args:
            event (S3IEvent): S3I event to check.

        Returns:
            bool: True if the handler is suited, False otherwise.
        """
        ...

    async def handle(self, event: S3IEvent) -> None:
        """Handle an incoming S3I event.

        Args:
            event (S3IEvent): S3I event to handle.
        """
        ...


@overload
def _find_suitable_handlers(
    handlers: list[MessageHandler], message: S3IMessageType
) -> list[MessageHandler]: ...


@overload
def _find_suitable_handlers(
    handlers: list[EventHandler], message: S3IEvent
) -> list[EventHandler]: ...


def _find_suitable_handlers(
    handlers: list[MessageHandler] | list[EventHandler], message: S3IMessageType | S3IEvent
) -> list[MessageHandler | EventHandler]:
    """Find all suitable handlers for the given message.

    Args:
        handlers (list[MessageHandler] | list[EventHandler]): List of message handlers.
        message (S3IMessageType | S3IEvent): S3I message to check.

    Returns:
        list[MessageHandler | EventHandler]: List of suitable handlers.
    """
    possible_handlers = [handler for handler in handlers if handler.is_suited(message)]
    if not possible_handlers:
        logger.warning(f"No suitable handlers found for message: {message}")
    elif len(possible_handlers) == 1:
        logger.debug(f"Found suitable handler: {possible_handlers[0].name}")
    else:
        logger.warning(
            f"Multiple handlers found for message: {message}. "
            f"Handlers: {", ".join(handler.name for handler in possible_handlers)}"
        )
    return possible_handlers


class S3IProcessor:
    """S³I message processor class."""

    def __init__(self) -> None:
        """Initialize the S3I processor."""
        self._message_handlers: list[MessageHandler] = []
        self._event_handlers: list[EventHandler] = []
        self._running_tasks: set[asyncio.Task] = set()

    def add_message_handler(self, handler: MessageHandler) -> None:
        """Add a new message handler."""
        if not isinstance(handler, MessageHandler):
            raise ValueError("Handler must implement the MessageHandler protocol.")
        self._message_handlers.append(handler)

    def add_event_handler(self, handler: EventHandler) -> None:
        """Add a new event handler."""
        if not isinstance(handler, EventHandler):
            raise ValueError("Handler must implement the EventHandler protocol.")
        self._event_handlers.append(handler)

    async def process_message(self, message: S3IMessageType) -> None:
        """Process a new S3I message."""
        handlers = await _find_suitable_handlers(self._message_handlers, message)
        for handler in handlers:
            task = asyncio.create_task(self._run_handler(handler, message))
            self._running_tasks.add(task)
            task.add_done_callback(self._running_tasks.discard)  # Remove task when done

    async def process_event(self, event: S3IEvent) -> None:
        """Process a new S3I event."""
        handlers = await _find_suitable_handlers(self._event_handlers, event)
        for handler in handlers:
            task = asyncio.create_task(self._run_handler(handler, event))
            self._running_tasks.add(task)
            task.add_done_callback(self._running_tasks.discard)  # Remove task when done

    async def _run_handler(
        self, handler: MessageHandler | EventHandler, message: S3IMessageType | S3IEvent
    ) -> None:
        """Wrapper to log start and end of handler execution."""
        logger.debug(f"Handler {handler.name} started processing message: {message}")
        with logger.catch():
            await handler.handle(message)
        logger.debug(f"Handler {handler.name} finished processing message: {message}")

    def get_running_handlers(self) -> list[str]:
        """Return a list of currently running handlers."""
        return [task.get_coro().__self__.name for task in self._running_tasks if not task.done()]
