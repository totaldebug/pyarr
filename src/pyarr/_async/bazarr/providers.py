from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray


class Providers(CommonActions):
    """Subtitle provider actions for Bazarr."""

    async def get(self) -> JsonArray:
        """Returns the list of subtitle providers.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("providers")
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'providers' endpoint")
