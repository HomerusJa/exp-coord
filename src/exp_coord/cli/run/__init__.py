import typer
from loguru import logger

from .all import all_app
from .forever import forever
from .setup import startup
from .single import single_app

app = typer.Typer()
app.callback()(startup)

app.add_typer(all_app)
app.add_typer(single_app)
app.command()(forever)


@app.command()
def test(ctx: typer.Context) -> None:
    """Run a test to check if setup and teardown works correctly."""
    logger.info("Running test...")
