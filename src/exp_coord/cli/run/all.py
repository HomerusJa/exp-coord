import typer

all_app = typer.Typer(
    name="all", help="Run the specified pipeline until all messages have been processed."
)


@all_app.command()
def message(ctx: typer.Context) -> None:
    """Process all messages from the queue."""


@all_app.command()
def event(ctx: typer.Context) -> None:
    """Process a single event from the queue."""
