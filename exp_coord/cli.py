"""
File providing the functionality to parse the args.
"""

import click
import click_log
import logging

logger = logging.getLogger("exp-coord")
click_log.basic_config(logger)


__all__ = ["cli"]


@click.group()
@click_log.simple_verbosity_option(logger, "-v", "--verbosity")
def cli() -> None:
    logger.info("Starting the program")


@cli.command()
def run():
    logger.info("Running the program")
