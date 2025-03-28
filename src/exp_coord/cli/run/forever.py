import typer
from loguru import logger


def forever(ctx: typer.Context) -> None:
    """Start the experiment coordinator and run it forever, or until the messages ran out."""
    logger.info("Starting experiment coordinator...")

    ctx.obj["broker_client"]
    ctx.obj["message_processor"]
    ctx.obj["event_processor"]
    ctx.obj["async_runner"]

    raise NotImplementedError()
