from httpx import Response
from pydantic import BaseModel, ValidationError

from exp_coord.services.s3i.base.error import BaseS3IError


class ErrorSchema(BaseModel):
    """Error response schema as defined at https://broker.s3i.vswf.dev/apidoc/."""

    error: str


class S3IBrokerError(BaseS3IError):
    """S3I broker error."""

    def __init__(self, response: Response, error: ErrorSchema | None) -> None:
        self.response = response
        self.error = error if error else ErrorSchema(error="Unknown error")

    def __str__(self) -> str:
        return f"[{self.response.status_code}]: {self.error.error}"


async def raise_on_error(response: Response):
    """Raise an S3IBrokerError if the response is an error."""
    if not response.is_error:
        return

    try:
        error = ErrorSchema.model_validate_json(response.content)
    except ValidationError:
        error = None
    raise S3IBrokerError(response, error)
