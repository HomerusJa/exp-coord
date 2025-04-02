from httpx import Response
from pydantic import BaseModel, TypeAdapter, ValidationError


class ErrorSchema(BaseModel):
    """Error response schema."""

    error: str


class ErrorMessageSchema(BaseModel):
    """Another error response schema. They seemingly couldn't agree on one (-:"""

    error_message: str


_ErrorSchemaTypes = ErrorSchema | ErrorMessageSchema
_ErrorSchemaAdapter = TypeAdapter(_ErrorSchemaTypes)


class S3IError(Exception):
    """S3I error."""

    def __init__(self, response: Response, error: _ErrorSchemaTypes | None) -> None:
        self.response = response
        self.error = error if error else ErrorSchema(error="Unknown error")

    def __str__(self) -> str:
        return f"[{self.response.status_code}]: {self.error.error}"


async def raise_on_error(response: Response):
    """Raise an S3IError if the response is an error."""
    if not response.is_error:
        return

    try:
        error = _ErrorSchemaAdapter.validate_json(response.content)
    except ValidationError:
        error = None
    raise S3IError(response, error)
