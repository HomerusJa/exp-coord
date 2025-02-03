import typer
from exp_coord.core.log import setup_logging

app = typer.Typer(name="exp_coord")


@app.command()
def run():
    typer.echo("Running once")


@app.command()
def run_forever():
    typer.echo("Running forever")


if __name__ == "__main__":
    setup_logging()
    app()
