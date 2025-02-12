"""Various utility functions to make working with typer easier."""

import sys
from functools import wraps

import click


def skip_execution_on_help_or_completion(func):
    """Decorator to prevent the command from running when the user asks for help or completion."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        ctx = click.get_current_context()
        if ctx.resilient_parsing or any(name in sys.argv[1:] for name in ctx.help_option_names):
            return
        return func(*args, **kwargs)

    return wrapper
