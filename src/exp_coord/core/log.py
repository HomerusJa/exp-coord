import logging
from loguru import logger

import inspect
import sys


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages and redirect them to Loguru.

    This class is taken directly from the Loguru documentation:
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # If the issuer is httpcore or httpx and the level is DEBUG, set the level to TRACE.
        if record.name.startswith("httpcore.") or record.name.startswith("httpx."):
            level = "TRACE" if level == "DEBUG" or level == 10 else level

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    logger.remove()
    logger.add(sys.stderr, level="TRACE")
    # TODO: Add a file handler here if needed.


# TODO: Remove this
setup_logging()
