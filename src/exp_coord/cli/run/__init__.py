import typer
from structlog.stdlib import get_logger

from .all import all_app
from .forever import forever_app
from .setup import startup
from .single import single_app

logger = get_logger(__name__)

app = typer.Typer()
app.callback()(startup)

app.add_typer(all_app)
app.add_typer(single_app)
app.add_typer(forever_app)


@app.command()
def test(ctx: typer.Context) -> None:
    """Run a test to check if setup and teardown works correctly."""
    logger.info("Running test...")
