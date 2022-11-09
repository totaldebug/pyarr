from typing import TypeVar, Union

JsonDataType = TypeVar(
    "JsonDataType", bound=Union[str, int, float, list, dict, bool, None]
)

_ReturnType = TypeVar("_ReturnType", bound=Union[dict, list])
