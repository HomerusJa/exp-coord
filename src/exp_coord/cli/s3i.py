"""Contains subcommands for playing around with S3I."""

import asyncio
from functools import wraps

import typer

from exp_coord.core.config import get_settings
from exp_coord.services.s3i import S3IBrokerClient
from exp_coord.services.s3i.config import S3IConfigClient

app = typer.Typer()
message_app = typer.Typer(name="message")
event_app = typer.Typer(name="event")

app.add_typer(message_app)
app.add_typer(event_app)


def async_command(func):
    """Decorator to handle async commands."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        async def _run():
            await func(*args, **kwargs)

        asyncio.run(_run())

    return wrapper


@app.command("get-token")
@async_command
async def get_token() -> None:
    settings = get_settings().s3i
    async with S3IConfigClient(settings) as client:
        token = await client.auth.get_valid_token()
    print(token)


@message_app.command("get")
@async_command
async def get_message() -> None:
    """Get a message from the message queue."""
    settings = get_settings().s3i
    async with S3IBrokerClient(settings) as client:
        message = await client.receive_message()
        print(message)


@message_app.command("send")
@async_command
async def send_message(endpoint: str, content: str) -> None:
    """Send a message to the message queue."""
    settings = get_settings().s3i
    async with S3IBrokerClient(settings) as client:
        # FIXME: Check whether validate_call really converts content from a string
        await client.send_message(endpoint=endpoint, message=content)  # type: ignore[reportArgumentType]


@event_app.command("get")
@async_command
async def get_event() -> None:
    """Get an event from the event queue."""
    settings = get_settings().s3i
    async with S3IBrokerClient(settings) as client:
        event = await client.receive_event()
        print(event)


@event_app.command("send")
@async_command
async def send_event(content: str) -> None:
    """Send an event to the event queue."""
    settings = get_settings().s3i
    async with S3IBrokerClient(settings) as client:
        # FIXME: Check whether validate_call really converts content from a string
        await client.send_event(content)  # type: ignore[reportArgumentType]


@event_app.command("add-topic")
@async_command
async def add_topic(topic: str) -> None:
    """Subscribe to a topic."""
    settings = get_settings().s3i
    async with S3IConfigClient(settings) as client:
        await client.add_thing_event_topic(settings.client_id, topic)
