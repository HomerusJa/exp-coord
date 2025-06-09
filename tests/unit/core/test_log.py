import logging

import pytest
import structlog

from exp_coord.core.log import (  # replace 'your_module' with actual module name
    LibraryLogFilter,
    add_callsite,
    field_to_str,
    setup_logging,
    truncate_long_field,
)


@pytest.fixture
def logger_setup():
    setup_logging()
    logger = structlog.get_logger()
    return logger


def test_library_log_filter_excludes_pymongo():
    record = logging.LogRecord(
        name="pymongo.something",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test",
        args=(),
        exc_info=None,
    )
    filter = LibraryLogFilter()
    assert not filter.filter(record)


def test_library_log_filter_includes_other():
    record = logging.LogRecord(
        name="myapp.module",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test",
        args=(),
        exc_info=None,
    )
    filter = LibraryLogFilter()
    assert filter.filter(record)


def test_field_to_str_with_bytes():
    processor = field_to_str("content")
    event_dict = {"content": b"hello world"}
    result = processor(None, None, event_dict)
    assert result["content"] == "hello world"


def test_field_to_str_with_str():
    processor = field_to_str("content")
    event_dict = {"content": "already a string"}
    result = processor(None, None, event_dict)
    assert result["content"] == "already a string"


def test_field_to_str_with_pydantic_model():
    class DummyModel:
        def model_dump_json(self):
            return '{"field": "value"}'

    processor = field_to_str("content")
    event_dict = {"content": DummyModel()}
    result = processor(None, None, event_dict)
    assert result["content"] == '{"field": "value"}'


def test_truncate_long_field():
    processor = truncate_long_field("content", 10)
    event_dict = {"content": "1234567890ABCDE"}
    result = processor(None, None, event_dict)
    assert result["content"] == "1234567890..."


def test_add_callsite():
    event_dict = {"logger": "my.module", "func_name": "myfunc", "lineno": 42}
    result = add_callsite(None, None, event_dict)
    assert result["callsite"] == "my.module:myfunc:42"


def test_setup_logging_console_output(capsys):
    setup_logging()
    logger = structlog.get_logger("test_logger")
    logger.info("Test event", content="Test content")

    captured = capsys.readouterr()
    assert "Test event" in captured.err
    assert "Test content" in captured.err

    structlog.reset_defaults()
