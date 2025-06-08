from pydantic import TypeAdapter

from exp_coord.core.utils import _get_type_adapter


def test_type_adapter_creation():
    adapter = _get_type_adapter(int)
    assert isinstance(adapter, TypeAdapter)
    assert adapter.validate_python(42) == 42
    assert adapter.dump_python(42) == 42


def test_type_adapter_caching():
    adapter1 = _get_type_adapter(int)
    adapter2 = _get_type_adapter(int)
    adapter3 = _get_type_adapter(str)

    assert adapter1 is adapter2  # Cached instance should be the same
    assert adapter1 is not adapter3  # Different types should have different instances


def test_print_logging(log_output):
    _get_type_adapter(float)  # First call should log
    _get_type_adapter(float)  # Cached call should not log again as it is cached

    assert len(log_output.entries) == 1
