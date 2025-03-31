import asyncio
from time import sleep

import typer
from loguru import logger

from exp_coord.services.s3i import (
    EventProcessor,
    MessageProcessor,
    S3IBrokerClient,
)


def forever(ctx: typer.Context, interval: int = 60, exit_on_failure: bool = True) -> None:
    """Start the experiment coordinator and run it forever, or until the messages ran out."""
    logger.info("Starting experiment coordinator...")

    broker_client: S3IBrokerClient = ctx.obj["broker_client"]
    event_processor: EventProcessor = ctx.obj["event_processor"]
    message_processor: MessageProcessor = ctx.obj["message_processor"]
    async_runner: asyncio.Runner = ctx.obj["async_runner"]

    @logger.catch(
        message="An error occurred during the current processing cycle",
        level="ERROR",
        reraise=exit_on_failure,
    )
    async def cycle():
        logger.info("Receiving all messages and events...")
        messages, events = await asyncio.gather(
            broker_client.receive_all_messages(), broker_client.receive_all_events()
        )

        logger.info(f"Processing {len(messages)} messages and {len(events)} events")
        await asyncio.gather(
            message_processor.process_all(messages), event_processor.process_all(events)
        )
        logger.success("Finished a cycle without errors.")

    while True:
        async_runner.run(cycle())
        logger.trace(f"Sleeping for {interval} seconds...")
        sleep(interval)
