import typer
from typer.testing import CliRunner

from exp_coord.cli.utils import skip_execution_on_help_or_completion

runner = CliRunner()


def test_skip_execution_decorator():
    app = typer.Typer()
    execution_count = 0

    # Create a test command that we'll decorate
    @app.command()
    @skip_execution_on_help_or_completion
    def test_command():
        nonlocal execution_count
        execution_count += 1
        return "Command executed"

    # Test 1: Normal execution
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert execution_count == 1

    # Test 2: Help flag shouldn't increment counter
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert execution_count == 1  # Should not have increased


def test_decorated_function_preserves_metadata():
    """Test that the decorator preserves the original function's metadata"""

    @skip_execution_on_help_or_completion
    def sample_func():
        """Sample docstring"""
        pass

    assert sample_func.__doc__ == "Sample docstring"
    assert sample_func.__name__ == "sample_func"


def test_decorator_with_arguments():
    app = typer.Typer()

    @app.command()
    @skip_execution_on_help_or_completion
    def command_with_args(name: str):
        print(f"Hello {name}")

    # Test normal execution with arguments
    result = runner.invoke(app, ["John"])
    assert result.exit_code == 0
    assert "Hello John" in result.stdout

    # Test help with arguments
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Hello" not in result.stdout
