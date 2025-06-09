import asyncio

import typer
from structlog.stdlib import get_logger

from exp_coord.services.s3i import EventProcessor, MessageProcessor, S3IBrokerClient

logger = get_logger(__name__)

single_app = typer.Typer(
    help="Run the message processing pipeline a single time.", no_args_is_help=True, name="single"
)


@single_app.command()
def message(ctx: typer.Context) -> None:
    """Process a single message from the queue."""
    logger.info("Running message processing...")

    broker_client: S3IBrokerClient = ctx.obj["broker_client"]
    message_processor: MessageProcessor = ctx.obj["message_processor"]
    async_runner: asyncio.Runner = ctx.obj["async_runner"]

    async def process_message() -> None:
        logger.debug("Fetching one message")
        message = await broker_client.receive_message()
        if message is not None:
            logger.debug("Processing message", content=message)

            await message_processor.process(message)
        else:
            logger.info("No messages to process")

    async_runner.run(process_message())


@single_app.command()
def event(ctx: typer.Context) -> None:
    """Process a single event from the queue."""
    logger.info("Running event processing...")

    broker_client: S3IBrokerClient = ctx.obj["broker_client"]
    event_processor: EventProcessor = ctx.obj["event_processor"]
    async_runner: asyncio.Runner = ctx.obj["async_runner"]

    async def process_event() -> None:
        logger.debug("Fetching one event")
        event = await broker_client.receive_event()
        if event is not None:
            logger.debug("Processing event", content=event)

            await event_processor.process(event)
        else:
            logger.info("No events to process")

    async_runner.run(process_event())
