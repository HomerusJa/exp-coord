from httpx import Response
from pydantic import BaseModel, Field, ValidationError


class ErrorSchema(BaseModel):
    """Unified error response schema with alias support."""

    error: str = Field(..., alias="error_message")


class S3IError(Exception):
    """S3I error."""

    def __init__(self, response: Response, error: ErrorSchema | bytes | None) -> None:
        self.response = response
        self.error = error if error else "Unknown error"

    def __str__(self) -> str:
        return f"[{self.response.status_code}]: {self.error}"


async def raise_on_error(
    response: Response, extend_allowed_response_codes: list[int] | None = None
) -> None:
    """Raise an S3IError if the response is an error."""
    if (
        extend_allowed_response_codes is not None
        and response.status_code in extend_allowed_response_codes
    ):
        return

    if not response.is_error:
        return

    try:
        error = ErrorSchema.model_validate_json(response.content)
    except ValidationError:
        error = response.content or None
    raise S3IError(response, error)
