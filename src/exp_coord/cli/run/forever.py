import asyncio
from time import sleep

import typer
from structlog.stdlib import get_logger

from exp_coord.services.s3i import (
    EventProcessor,
    MessageProcessor,
    S3IBrokerClient,
)

logger = get_logger(__name__)

forever_app = typer.Typer(
    name="forever",
    invoke_without_command=True,
)


@forever_app.callback()
def forever(ctx: typer.Context, interval: int = 60, exit_on_failure: bool = True) -> None:
    """Start the experiment coordinator and run it forever, or until the messages run out."""
    logger.info("Starting experiment coordinator...")

    broker_client: S3IBrokerClient = ctx.obj["broker_client"]
    event_processor: EventProcessor = ctx.obj["event_processor"]
    message_processor: MessageProcessor = ctx.obj["message_processor"]
    async_runner: asyncio.Runner = ctx.obj["async_runner"]

    async def cycle():
        logger.info("Receiving all messages and events...")
        messages, events = await asyncio.gather(
            broker_client.receive_all_messages(), broker_client.receive_all_events()
        )

        logger.info(f"Processing {len(messages)} messages and {len(events)} events")
        await asyncio.gather(
            message_processor.process_all(messages), event_processor.process_all(events)
        )
        logger.info("Finished a cycle without errors.")

    while True:
        try:
            async_runner.run(cycle())
        except:  # noqa: E722
            logger.error("An error occurred during the current processing cycle.", exc_info=True)
            if exit_on_failure:
                raise
        logger.debug(f"Sleeping for {interval} seconds...")
        sleep(interval)
