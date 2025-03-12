"""Contains subcommands for playing around with S3I."""

import asyncio
from functools import wraps

import typer

from exp_coord.cli.utils import skip_execution_on_help_or_completion
from exp_coord.core.config import get_settings
from exp_coord.services.s3i import S3IBrokerClient

app = typer.Typer()


def async_command(func):
    """Decorator to handle async commands."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        async def _run():
            await func(*args, **kwargs)

        asyncio.run(_run())

    return wrapper


@app.callback()
@skip_execution_on_help_or_completion
def startup(ctx: typer.Context) -> None:
    """Main entry point that sets up the S3I client."""
    ctx.ensure_object(dict)
    ctx.obj["s3i_client"] = S3IBrokerClient(get_settings().s3i)


@app.command()
@async_command
async def get_message(ctx: typer.Context) -> None:
    """Get a message from the message queue."""
    async with ctx.obj["s3i_client"] as client:
        message = await client.receive_message()
        print(message)


@app.command()
@async_command
async def get_event(ctx: typer.Context) -> None:
    """Get an event from the event queue."""
    async with ctx.obj["s3i_client"] as client:
        event = await client.receive_event()
        print(event)


@app.command()
@async_command
async def send_message(ctx: typer.Context, endpoint: str, content: str) -> None:
    """Send a message to the message queue."""
    async with ctx.obj["s3i_client"] as client:
        await client.send_message("Hello, World!")


@app.command()
@async_command
async def send_event(ctx: typer.Context, content: str) -> None:
    """Send an event to the event queue."""
    async with ctx.obj["s3i_client"] as client:
        await client.send_event(content)
