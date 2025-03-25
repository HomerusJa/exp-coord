import pytest


@pytest.mark.skip(
    reason="setup_database is currently broken. It doesnt set the database name correctly"
)
def test_setup(setup_database):
    """This is not more than a test verifying that the test infrastructure is set up correctly."""
    assert True
