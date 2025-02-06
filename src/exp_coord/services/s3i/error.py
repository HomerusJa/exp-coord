from meatie import AsyncResponse, ResponseError
from pydantic import BaseModel, ValidationError


class ErrorSchema(BaseModel):
    """Error response schema."""

    error: str


class S3IBrokerError(ResponseError):
    """S³I Broker error response."""

    def __init__(self, response: AsyncResponse, error_model: ErrorSchema | None = None) -> None:
        super().__init__(response)
        self.error = error_model.error if error_model else "Unknown error"
        self.status_code = response.status

    def __str__(self) -> str:
        return f"S3IBrokerError [{self.status_code}]: {self.error}"


async def get_error(response: AsyncResponse) -> Exception | None:
    """Get the error from the response."""
    if response.status <= 200 < 300:
        return None

    try:
        error = ErrorSchema.model_validate_json(await response.text())
    except ValidationError:
        error = None

    return S3IBrokerError(response, error)
