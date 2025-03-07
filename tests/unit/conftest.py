import pytest

import exp_coord.db.connection


def _raises_func(exception: Exception):
    def _raises_func(*args, **kwargs):
        raise exception

    return _raises_func


@pytest.fixture(autouse=True, scope="function")
def disallow_network_calls(monkeypatch):
    monkeypatch.setattr(
        exp_coord.db.connection,
        "get_db",
        _raises_func(
            RuntimeError("Getting a database should not be allowed as this is a unit test")
        ),
    )
    monkeypatch.setattr(
        exp_coord.db.connection,
        "get_client",
        _raises_func(RuntimeError("Getting a client should not be allowed as this is a unit test")),
    )
    monkeypatch.setattr(
        exp_coord.db.connection,
        "get_grid_fs_client",
        _raises_func(
            RuntimeError("Getting the GridFS client should not be allowed as this is a unit test")
        ),
    )
