import logging

import colorama
import structlog

__all__ = ["setup_logging"]


# TODO: Maybe change this to be logging.getLogger("pymongo").setLevel(logging.WARNING) and so on
class LibraryLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Use the fully qualified module path if available, else fallback to logger name
        module = getattr(record, "module", None)
        name = getattr(record, "name", "")
        return not (
            (module and (module.startswith("pymongo") or module.startswith("httpcore")))
            or name.startswith("pymongo")
            or name.startswith("httpcore")
        )


def field_to_str(field_name: str) -> structlog.typing.Processor:
    """Convert the given field to a string, using various conversion methods.

    Conversion rules:
    - str: left unchanged
    - bytes, bytearray: decoded to UTF-8 string (with errors replaced)
    - pydantic.BaseModel: converted to JSON string via `.model_dump_json()`
    - default: converted to string via `str()`
    """

    def processor(_, __, event_dict: structlog.typing.EventDict) -> structlog.typing.EventDict:
        content = event_dict.get(field_name, None)
        if content is not None:
            match content:
                case str():
                    pass  # Already a string, do nothing
                case (bytes() | bytearray()) as b:
                    content = b.decode("utf-8", errors="replace")
                case model if hasattr(model, "model_dump_json") and callable(model.model_dump_json):
                    # For Pydantic models or similar
                    content = model.model_dump_json()
                case _:
                    content = str(content)
            event_dict[field_name] = content
        return event_dict

    return processor


def truncate_long_field(field_name: str, max_len: int) -> structlog.typing.Processor:
    """Create a processor that truncates `field_name` if it is longer than `max_len` and a string."""

    def processor(_, __, event_dict: structlog.typing.EventDict) -> structlog.typing.EventDict:
        content = event_dict.get(field_name, None)
        if isinstance(content, str) and len(content) > max_len:
            content = content[:max_len] + "..."
            event_dict[field_name] = content
        return event_dict

    return processor


def add_callsite(_, __, event_dict: structlog.typing.EventDict) -> structlog.typing.EventDict:
    """Add the callsite to the event dictionary.

    This processor depends on two processors:
    1. structlog.stdlib.add_logger_name
    2. structlog.processors.CallsiteParameterAdder with the two parameters FUNC_NAME and LINENO
    """
    module = event_dict.pop("logger", "?")
    func_name = event_dict.pop("func_name", "?")
    lineno = event_dict.pop("lineno", "?")

    event_dict["callsite"] = f"{module}:{func_name}:{lineno}"
    return event_dict


SHARED_PROCESSORS = [
    structlog.stdlib.add_log_level,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.stdlib.add_logger_name,
    structlog.processors.CallsiteParameterAdder(
        [
            structlog.processors.CallsiteParameter.FUNC_NAME,
            structlog.processors.CallsiteParameter.LINENO,
        ]
    ),
    add_callsite,
    structlog.processors.format_exc_info,
    field_to_str("content"),
    truncate_long_field("content", max_len=500),
]


def _get_console_columns() -> list[structlog.dev.Column]:
    """Build and return the list of columns for the console renderer."""
    return [
        structlog.dev.Column(
            "timestamp",
            structlog.dev.KeyValueColumnFormatter(
                key_style=None,
                value_style=colorama.Fore.BLACK,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
        structlog.dev.Column(
            "level",
            structlog.dev.LogLevelColumnFormatter(
                level_styles={
                    "critical": colorama.Fore.RED,
                    "exception": colorama.Fore.RED,
                    "error": colorama.Fore.RED,
                    "warn": colorama.Fore.YELLOW,
                    "warning": colorama.Fore.YELLOW,
                    "info": colorama.Fore.WHITE,
                    "debug": colorama.Fore.BLUE,
                },
                reset_style=colorama.Style.RESET_ALL,
            ),
        ),
        structlog.dev.Column(
            "callsite",
            structlog.dev.KeyValueColumnFormatter(
                prefix="[",
                postfix="]",
                width=50,  # Maybe adjust, works for now
                key_style=None,
                value_style=colorama.Fore.GREEN,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
        structlog.dev.Column(
            "event",
            structlog.dev.KeyValueColumnFormatter(
                key_style=None,
                value_style=colorama.Fore.WHITE + colorama.Style.BRIGHT,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
        structlog.dev.Column(
            "",
            structlog.dev.KeyValueColumnFormatter(
                key_style=colorama.Fore.CYAN,
                value_style=colorama.Fore.GREEN,
                reset_style=colorama.Style.RESET_ALL,
                value_repr=str,
            ),
        ),
    ]


def _get_console_formatter() -> logging.Formatter:
    """Build and return the console formatter with custom structlog columns."""
    return structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=SHARED_PROCESSORS,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(columns=_get_console_columns()),
        ],
    )


def setup_logging():
    """Setup logging configuration

    Reference: https://www.structlog.org/en/stable/standard-library.html#rendering-using-structlog-based-formatters-within-logging
    """
    structlog.configure(
        processors=SHARED_PROCESSORS + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],  # noqa: RUF005
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    handler = logging.StreamHandler()
    handler.setFormatter(_get_console_formatter())
    handler.addFilter(LibraryLogFilter())

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]  # Ensure this is the only handler
    root_logger.setLevel(logging.DEBUG)
