"""Configure the root logger."""

from __future__ import annotations

import atexit
import datetime as dt
import json
import logging
import logging.config
import logging.handlers
from enum import Enum, auto
from pathlib import Path
from typing import Any, NotRequired, TypedDict, override

try:
    import tomllib
except ImportError:
    import tomli as tomllib  # type: ignore[import-not-found, no-redef]

from project_name.config import LOGGER_CONFIG_FILE, PACKAGE_NAME

ROOT_LOGGER_NAME = PACKAGE_NAME

__all__ = ('ROOT_LOGGER_NAME', 'setup_logging')


class RecordAttrs(str, Enum):
    """Log record attributes."""

    @override
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list) -> str:
        """Create enum values from the names automatically."""
        return name

    args = auto()
    asctime = auto()
    created = auto()
    exc_info = auto()
    exc_text = auto()
    filename = auto()
    funcName = auto()
    levelname = auto()
    levelno = auto()
    lineno = auto()
    module = auto()
    msecs = auto()
    message = auto()
    msg = auto()
    name: str = "name"
    pathname = auto()
    process = auto()
    processName = auto()
    relativeCreated = auto()
    stack_info = auto()
    thread = auto()
    threadName = auto()
    taskName = auto()


class FormatKeys(TypedDict):
    """Log format keys."""

    message: str
    timestamp: dt.datetime
    level: NotRequired[str]
    logger: NotRequired[str]
    module: NotRequired[str]
    function: NotRequired[str]
    line: NotRequired[int]
    thread_name: NotRequired[str]


class LogDict(FormatKeys):
    """Specify keys log entries can contain."""

    exc_info: NotRequired[str]
    stack_info: NotRequired[str]


class CustomQueueHandler(logging.handlers.QueueHandler):
    """Custom queue handler."""

    @override
    def __init__(self, *args: Any, **kwargs: dict[str, Any]) -> None:
        queue_handler = logging.getHandlerByName("queue_handler")
        if queue_handler is None:
            super().__init__(*args, **kwargs)
        else:
            queue_handler.listener.start()
            atexit.register(queue_handler.listener.stop)


class JSONLogFormatter(logging.Formatter):
    """Custom JSON log formatter."""

    @override
    def __init__(self, *, fmt_keys: FormatKeys | None = None) -> None:
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    @override
    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_log_dict(record)
        return json.dumps(message, default=str)

    def _prepare_log_dict(self, record: logging.LogRecord) -> LogDict:
        required_fields: LogDict = {
            'message': record.getMessage(),
            'timestamp': dt.datetime.fromtimestamp(
                record.created,
                tz=dt.timezone.utc,
            ),
        }

        if record.exc_info is not None:
            required_fields['exc_info'] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            required_fields['stack_info'] = self.formatStack(record.stack_info)

        message: LogDict = {
            key: msg_val
            if (msg_val := required_fields.pop(val, None)) is not None
            else getattr(record, val)
            for key, val in self.fmt_keys.items()
        }

        message.update(required_fields)

        for key, val in record.__dict__.items():
            if key not in RecordAttrs:
                message[key] = val

        return message


def setup_logging() -> None:
    """Set up logging."""
    (Path.cwd() / 'logs').mkdir(exist_ok=True)
    logger_data = LOGGER_CONFIG_FILE.read_text(encoding='utf-8')
    logging_config = tomllib.loads(logger_data)
    logging.config.dictConfig(logging_config)

    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler is not None:
        queue_handler.listener.start()  # type: ignore[attr-defined]
        atexit.register(queue_handler.listener.stop)  # type: ignore[attr-defined]
