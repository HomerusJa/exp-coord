# Just for typing purposes. I'm not using it in the actual code.
import _io
import logging

import click
import click_log

logger = logging.getLogger("exp-coord")
click_log.basic_config(logger)


@click.group()
@click_log.simple_verbosity_option(logger, "-v", "--verbosity", default="DEBUG")
def cli() -> None:
    """This is the coordinator for the experiment."""
    logger.info("Starting the program")


@cli.command()
@click.argument("config-file", type=click.File("r"))
def run(config_file: _io.TextIOWrapper) -> None:
    """Run the task given in the config file argument."""
    logger.info(f"Config file: {config_file.name}")


if __name__ == "__main__":
    cli()
