import asyncio
from typing import Annotated

import click
import typer
from loguru import logger

from exp_coord.cli.utils import skip_execution_on_help_or_completion
from exp_coord.core.config import settings
from exp_coord.core.log import setup_logging
from exp_coord.core.utils import syncify
from exp_coord.db.connection import init_db
from exp_coord.handlers import EVENT_HANDLERS, MESSAGE_HANDLERS
from exp_coord.services.s3i import EventProcessor, MessageProcessor, S3IBrokerClient

app = typer.Typer()


def shutdown() -> None:
    """Shutdown cleanup function to close broker client."""
    ctx = click.get_current_context()
    broker_client = ctx.obj.get("broker_client")
    if broker_client:
        logger.info("Closing broker client...")
        syncify(broker_client.close)()


@app.callback()
@skip_execution_on_help_or_completion
def startup(ctx: typer.Context) -> None:
    logger.debug(f"Using following settings: {settings}")
    setup_logging()
    syncify(init_db)()
    ctx.ensure_object(dict)
    ctx.obj["broker_client"] = S3IBrokerClient(settings.s3i)
    ctx.obj["event_processor"] = EventProcessor(EVENT_HANDLERS)
    ctx.obj["message_processor"] = MessageProcessor(MESSAGE_HANDLERS)

    ctx.call_on_close(shutdown)


@app.command()
def single(ctx: typer.Context, only_message: bool = False, only_event: bool = False) -> None:
    """Process just one message or event from the queue."""
    logger.info("Running...")

    broker_client: S3IBrokerClient = ctx.obj["broker_client"]
    event_processor: EventProcessor = ctx.obj["event_processor"]
    message_processor: MessageProcessor = ctx.obj["message_processor"]

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
        syncify(process_message)()
    if not only_message:
        asyncio.run(process_event())
    # TODO: Use something like gather here


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
    logger.info("Running forever...")
