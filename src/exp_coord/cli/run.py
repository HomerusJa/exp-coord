import asyncio
from typing import Annotated

import typer
from loguru import logger

from exp_coord.cli.utils import skip_execution_on_help_or_completion
from exp_coord.core.config import settings
from exp_coord.core.log import setup_logging
from exp_coord.db.connection import init_db

app = typer.Typer()


@app.callback()
@skip_execution_on_help_or_completion
def startup(ctx: typer.Context) -> None:
    logger.debug(f"Using following settings: {settings}")
    setup_logging()
    asyncio.run(init_db())


@app.command()
def single() -> None:
    """Process just one message or event from the queue."""
    logger.info("Running...")


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
