"""Main entry point, remove if project is not an executable."""

import logging

from project_name.logger import ROOT_LOGGER_NAME, setup_logging

logger = logging.getLogger(ROOT_LOGGER_NAME)


def main():
    """Main program."""
    setup_logging()
    # logging.basicConfig(level=logging.INFO)

    logger.debug("debug message", extra={'foo': 'hello'})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    try:
        1337 / 0
    except ZeroDivisionError:
        logger.error("exception message")


if __name__ == '__main__':
    main()
