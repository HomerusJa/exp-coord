from logot import Logot, logged
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


def test_print_logging(logot: Logot):
    _get_type_adapter(float)  # First call should print
    _get_type_adapter(float)  # Cached call should not print again

    logot.assert_logged(logged.debug("Creating cached TypeAdapter for <class 'float'>"))

    _get_type_adapter(float)  # Call again to check caching
    logot.assert_not_logged(logged.debug("Creating cached TypeAdapter for <class 'float'>"))
