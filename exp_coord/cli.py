"""
File providing the functionality to parse the args.
"""

import click
import click_log
import logging

logger = logging.getLogger("exp-coord")
click_log.basic_config(logger)


__all__ = ["cli"]


@click.command()
@click_log.simple_verbosity_option(logger)
def cli():
    logger.warning("TEST")
