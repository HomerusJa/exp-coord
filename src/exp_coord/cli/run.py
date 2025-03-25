import asyncio
from typing import Annotated

import click
import typer
from loguru import logger

from exp_coord.cli.utils import skip_execution_on_help_or_completion
from exp_coord.core.config import get_settings
from exp_coord.db.connection import close_db, get_client, init_db
from exp_coord.handlers import EVENT_HANDLERS, MESSAGE_HANDLERS
from exp_coord.services.s3i import EventProcessor, MessageProcessor, S3IBrokerClient

app = typer.Typer()


def _close_broker_client(ctx: click.Context) -> None:
    """Close the broker client."""
    async_runner: asyncio.Runner | None = ctx.obj.get("async_runner", None)
    broker_client: S3IBrokerClient | None = ctx.obj.get("broker_client", None)

    if broker_client is None:
        logger.debug("Broker client not initialized yet")
        return

    if async_runner is None:
        raise RuntimeError("Async runner not found, cannot close broker client")

    try:
        async_runner.get_loop()
    except RuntimeError as exc:
        if str(exc) == "Runner is closed":
            raise RuntimeError(
                "Async runner not initialized or has already been closed, cannot close broker client"
            ) from exc
        else:
            raise exc

    logger.trace("Closing broker client...")
    async_runner.run(broker_client.aclose())


def _close_db_connection(ctx: click.Context) -> None:
    try:
        _ = get_client()
    except RuntimeError as exc:
        if str(exc) == "Database connection not established":
            logger.debug("Database connection was not established yet")
            return
        else:
            raise exc

    async_runner: asyncio.Runner | None = ctx.obj.get("async_runner", None)
    if async_runner is None:
        raise RuntimeError("Async runner not initialized, cannot close database connection")
    async_runner.run(close_db())


def shutdown() -> None:
    """Shutdown cleanup function."""
    logger.info("Entering shutdown procedure")
    ctx = click.get_current_context()

    with logger.catch(message="Error while closing broker client"):
        _close_broker_client(ctx)
        logger.info("Closed broker client")

    with logger.catch(message="Error while closing the database connection"):
        _close_db_connection(ctx)
        logger.info("Closed database connection")

    with logger.catch(message="Error while closing async runner"):
        async_runner: asyncio.Runner | None = ctx.obj.get("async_runner", None)
        if async_runner is not None:
            async_runner.close()
        logger.info("Closed async runner")

    logger.success("Shutdown complete")


@app.callback()
@skip_execution_on_help_or_completion
def startup(ctx: typer.Context) -> None:
    ctx.call_on_close(shutdown)

    logger.debug(f"Using following settings: {get_settings()}")

    ctx.ensure_object(dict)
    ctx.obj["broker_client"] = S3IBrokerClient(get_settings().s3i)
    ctx.obj["event_processor"] = EventProcessor(EVENT_HANDLERS)
    ctx.obj["message_processor"] = MessageProcessor(MESSAGE_HANDLERS)
    # Can't use ctx.with_resource as it closes the runner before shutdown is called. We need to now close it manually
    ctx.obj["async_runner"] = asyncio.Runner()

    ctx.obj["async_runner"].run(init_db())


@app.command()
def test(ctx: typer.Context) -> None:
    """Run a test to check if setup and teardown works correctly."""
    logger.info("Running test...")


@app.command()
def single(ctx: typer.Context, only_message: bool = False, only_event: bool = False) -> None:
    """Process just one message or event from the queue."""
    logger.info("Running...")

    broker_client: S3IBrokerClient = ctx.obj["broker_client"]
    event_processor: EventProcessor = ctx.obj["event_processor"]
    message_processor: MessageProcessor = ctx.obj["message_processor"]
    async_runner: asyncio.Runner = ctx.obj["async_runner"]

    async def process_message() -> None:
        logger.debug("Fetching one message")
        message = await broker_client.receive_message()
        if message is not None:
            logger.debug(f"Processing message: {message}")
            await message_processor.process(message)
        else:
            logger.info("No messages to process")

    async def process_event() -> None:
        logger.debug("Fetching one event")
        event = await broker_client.receive_event()
        if event is not None:
            logger.debug(f"Processing event: {event}")
            await event_processor.process(event)
        else:
            logger.info("No events to process")

    if not only_event:
        async_runner.run(process_message())
    if not only_message:
        async_runner.run(process_event())


@app.command()
def forever(
    stop_when_empty: Annotated[
        bool,
        typer.Option(
            help="Should the experiment coordinator stop when it doesn't receive any messages anymore?"
        ),
    ] = True,
) -> None:
    """Start the experiment coordinator and run it forever, or until the messages ran out."""
    raise NotImplementedError("Forever mode not yet implemented")
