from functools import cache
from typing import TypeVar

from loguru import logger
from pydantic import TypeAdapter

T = TypeVar("T")


@cache
def _get_type_adapter(type_: T) -> TypeAdapter[T]:
    """Create a cached TypeAdapter instance for a type. The caching is the only reason for this function to exist."""
    logger.debug(f"Creating cached TypeAdapter for {type_}")
    return TypeAdapter(type_)
