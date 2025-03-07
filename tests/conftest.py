import pytest

from exp_coord.core.config import update_settings


@pytest.fixture(scope="session", autouse=True)
def use_test_database():
    update_settings({"mongodb": {"db_name": "exp-coord-test"}})
