import inspect
import logging

import structlog

__all__ = ["setup_logging"]


class LibraryLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        # Use the fully qualified module path if available, else fallback to logger name
        module = getattr(record, "module", None)
        name = getattr(record, "name", "")
        return (
            (module and (module.startswith("pymongo") or module.startswith("httpcore")))
            or name.startswith("pymongo")
            or name.startswith("httpcore")
        )


def add_module_path(_, __, event_dict):
    # Walk the stack to find the first frame outside structlog/logging internals
    if event_dict.get("module"):
        raise RuntimeError("module key already exists in event dict")

    frame = inspect.currentframe()
    while frame:
        module = inspect.getmodule(frame)
        # Skip frames from structlog and logging
        if (
            module
            and not module.__name__.startswith(("structlog", "logging"))
            and module.__name__ != "exp_coord.core.log"
        ):
            event_dict["module"] = module.__name__
            break
        frame = frame.f_back
    return event_dict


def setup_logging():
    """Setup logging configuration

    Reference: https://www.structlog.org/en/stable/standard-library.html#rendering-using-structlog-based-formatters-within-logging
    """
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        add_module_path,
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            ]
        ),
        structlog.processors.format_exc_info,
    ]
    structlog.configure(
        processors=shared_processors + [structlog.stdlib.ProcessorFormatter.wrap_for_formatter],  # noqa: RUF005
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        # These run ONLY on `logging` entries that do NOT originate within
        # structlog.
        foreign_pre_chain=shared_processors,
        # These run on ALL entries after the pre_chain is done.
        processors=[
            # Remove _record & _from_structlog.
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(),
        ],
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.addFilter(LibraryLogFilter())

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)
