import pytest
from meatie import AsyncResponse
from pydantic import ValidationError
from exp_coord.services.s3i.error import (
    ErrorSchema,
    S3IBrokerError,
    get_error,
)


@pytest.fixture
def mock_response(mocker):
    """Fixture to create a mock AsyncResponse."""

    def _mock_response(status, text):
        response = mocker.Mock(spec=AsyncResponse)
        response.status = status
        response.text = mocker.AsyncMock(return_value=text)
        return response

    return _mock_response


@pytest.mark.asyncio
async def test_get_error_no_error(mock_response):
    """Test get_error when the response status is successful."""
    response = mock_response(200, '{"key": "value"}')  # Any valid response body
    error = await get_error(response)
    assert error is None


@pytest.mark.asyncio
async def test_get_error_with_valid_error(mock_response):
    """Test get_error with a valid error response."""
    response = mock_response(400, '{"error": "Something went wrong"}')
    error = await get_error(response)

    assert isinstance(error, S3IBrokerError)
    assert error.error == "Something went wrong"
    assert error.status_code == 400
    assert str(error) == "S3IBrokerError [400]: Something went wrong"


@pytest.mark.asyncio
async def test_get_error_with_invalid_error(mock_response, mocker):
    """Test get_error with an invalid error response."""
    response = mock_response(400, '{"invalid": "data"}')

    # Simulate a ValidationError with properly constructed raw_errors
    mocker.patch.object(
        ErrorSchema,
        "model_validate_json",
        side_effect=ValidationError.from_exception_data("", []),
    )

    error = await get_error(response)

    assert isinstance(error, S3IBrokerError)
    assert error.error == "Unknown error"
    assert error.status_code == 400
    assert str(error) == "S3IBrokerError [400]: Unknown error"


@pytest.mark.asyncio
async def test_get_error_with_non_json_response(mock_response):
    """Test get_error with a non-JSON response body."""
    response = mock_response(500, "Internal Server Error")

    error = await get_error(response)

    assert isinstance(error, S3IBrokerError)
    assert error.error == "Unknown error"
    assert error.status_code == 500
    assert str(error) == "S3IBrokerError [500]: Unknown error"
