import asyncio
import functools


def syncify(func):
    """Wrap an async function so it can be called synchronously."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            return asyncio.create_task(func(*args, **kwargs))
        else:
            return asyncio.run(func(*args, **kwargs))

    return wrapper
