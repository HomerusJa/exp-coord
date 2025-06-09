import pytest
import typer
from typer.testing import CliRunner

from exp_coord.cli.utils import skip_execution_on_help_or_completion


@pytest.fixture(scope="module")
def runner():
    return CliRunner()


@pytest.fixture(scope="module")
def typer_app():
    app = typer.Typer()

    @app.callback()
    @skip_execution_on_help_or_completion
    def _():
        print("Callback ran")

    @app.command()
    def hello(name: str):
        print(f"Hello {name}")

    return app


def test_run_happy_path(runner, typer_app):
    result = runner.invoke(typer_app, ["hello", "John"])
    assert result.exit_code == 0
    assert "Callback ran" in result.stdout
    assert "Hello John" in result.stdout


def test_run_help(runner, typer_app):
    result = runner.invoke(typer_app, ["--help"])
    assert result.exit_code == 0
    assert "Callback ran" not in result.stdout
    assert "Hello John" not in result.stdout
