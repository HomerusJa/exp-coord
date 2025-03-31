import asyncio

import typer

from exp_coord.services.s3i import EventProcessor, MessageProcessor, S3IBrokerClient

all_app = typer.Typer(
    name="all", help="Run the specified pipeline until all messages have been processed."
)


@all_app.command()
def message(ctx: typer.Context) -> None:
    """Process all messages from the queue."""

    broker_client: S3IBrokerClient = ctx.obj["broker_client"]
    message_processor: MessageProcessor = ctx.obj["message_processor"]
    async_runner: asyncio.Runner = ctx.obj["async_runner"]

    messages = async_runner.run(broker_client.receive_all_messages())
    async_runner.run(message_processor.process_all(messages))


@all_app.command()
def event(ctx: typer.Context) -> None:
    """Process all events from the queue."""

    broker_client: S3IBrokerClient = ctx.obj["broker_client"]
    event_processor: EventProcessor = ctx.obj["event_processor"]
    async_runner: asyncio.Runner = ctx.obj["async_runner"]

    events = async_runner.run(broker_client.receive_all_events())
    async_runner.run(event_processor.process_all(events))
