from typing import Any, TypeVar

JsonDataType = Any
JsonObject = dict[str, Any]
JsonArray = list[JsonObject]

_ReturnType = TypeVar("_ReturnType", bound=dict | list)

__all__ = ["JsonArray", "JsonObject", "JsonDataType"]
