from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray


class Update(CommonActions):
    """Update actions for Arr clients."""

    async def get(self) -> JsonArray:
        """Returns the list of available updates.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("update")
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'update' endpoint")
