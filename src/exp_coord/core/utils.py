from typing import TypeVar, Generic, Protocol
from pydantic import TypeAdapter


class PydanticModel(Protocol):
    def model_validate(self, obj): ...

    def model_validate_json(self, json_str: str): ...

    def model_dump(self, obj): ...

    def model_dump_json(self, obj): ...


T = TypeVar("T")


class TypeAdapterWrapper(Generic[T]):
    """Wrapper for TypeAdapter to use it like a BaseModel.

    Usage:
        type_adapter = TypeAdapter(list[int])
        wrapped = TypeAdapterWrapper(type_adapter)

        # Now you can use it like a BaseModel:
        validated = wrapped.model_validate([1, 2, 3])
        json_validated = wrapped.model_validate_json("[1, 2, 3]")
    """

    def __init__(self, type_adapter: TypeAdapter[T]):
        self._adapter = type_adapter

    def model_validate(self, obj):
        return self._adapter.validate_python(obj)

    def model_validate_json(self, json_str: str):
        return self._adapter.validate_json(json_str)

    def model_dump(self, obj):
        return self._adapter.dump_python(obj)

    def model_dump_json(self, obj):
        return self._adapter.dump_json(obj)
