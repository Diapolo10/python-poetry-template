"""Main entry point, remove if project is not an executable."""

import logging

from project_name.logger import ROOT_LOGGER_NAME, setup_logging

logger = logging.getLogger(ROOT_LOGGER_NAME)


def main() -> None:
    """Lorem Ipsum."""
    setup_logging()

    logger.debug("debug message", extra={"foo": "hello"})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    try:
        _ = 1337 / 0
    except ZeroDivisionError:
        logger.exception("exception message")


if __name__ == "__main__":
    main()
