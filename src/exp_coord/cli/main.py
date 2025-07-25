import typer

from exp_coord.cli.data import app as data_app
from exp_coord.cli.run import app as run_app
from exp_coord.cli.s3i import app as s3i_app
from exp_coord.cli.utils import skip_execution_on_help_or_completion
from exp_coord.core.log import setup_logging

app = typer.Typer(
    help="Your friendly CLI interface for the experiment coordinator.",
    no_args_is_help=True,
)


@app.callback()
@skip_execution_on_help_or_completion
def setup():
    setup_logging()


app.add_typer(
    s3i_app,
    name="s3i",
    help="Play around with S3I. This wont invoke any reactions afterwards, as when using the run commands.",
    no_args_is_help=True,
)
app.add_typer(
    run_app,
    name="run",
    help="Run the experiment coordinator, either just once or as a server.",
    no_args_is_help=True,
)
app.add_typer(
    data_app,
    name="data",
    help="Work with the experiment data.",
    no_args_is_help=True,
)
