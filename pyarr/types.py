from typing import TypeVar, Union

JsonDataType = TypeVar(
    "JsonDataType", bound=Union[str, int, float, list, dict, bool, None]
)
