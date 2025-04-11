from functools import cache
from typing import TypeVar

from loguru import logger
from pydantic import TypeAdapter

T = TypeVar("T")


@cache
def _get_type_adapter(type_: T) -> TypeAdapter[T]:
    """Create a cached TypeAdapter instance for a type. The caching is the only reason for this function to exist."""
    # FIXME: If type_ is not hashable, the cache will raise a TypeError
    logger.debug(f"Creating cached TypeAdapter for {type_}")
    return TypeAdapter(type_)
