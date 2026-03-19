from pyarr.common.base import CommonActions
from pyarr.types import JsonArray


class CustomFilter(CommonActions):
    """Custom filter actions for Radarr."""

    def get(self) -> JsonArray:
        """Query Radarr for custom filters.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = self.handler.request("customfilter")
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'customfilter' endpoint")
