from apscheduler.schedulers.blocking import BlockingScheduler

import logging

logger = logging.getLogger("exp-coord")

from cli import cli


def main():
    """
    Main entry point of the program

    Args:
        args (list): The arguments that were given to the application. You want
            most of the time, that those are sys.argv.
    """
    cli()


if __name__ == "__main__":
    main()
