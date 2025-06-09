"""Various utility functions to make working with typer easier."""

from functools import wraps

import click


def skip_execution_on_help_or_completion(func):
    """Decorator to prevent the command from running when the user asks for help or completion."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        if ctx.invoked_subcommand is None or "--help" in ctx.args:
            return
        return func(*args, **kwargs)

    return wrapper
