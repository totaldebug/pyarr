from typing import TypeVar, Union

JsonDataType = TypeVar(
    "JsonDataType", bound=Union[str, int, float, list, dict, bool, None]
)

JsonObject = dict[str, JsonDataType]
JsonArray = list[JsonObject]

_ReturnType = TypeVar("_ReturnType", bound=Union[dict, list])

__all__ = [_ReturnType, JsonArray]
