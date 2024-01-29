from click.testing import CliRunner
from cli import cli

def test_logging_cli():
    runner = CliRunner()
    result = runner.invoke()