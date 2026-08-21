from pyarr._async.common.base import CommonActions
from pyarr.types import JsonObject


class Providers(CommonActions):
    """Subtitle provider actions for Bazarr."""

    async def get(self) -> JsonObject:
        """Returns the subtitle providers Bazarr knows about.

        Returns:
            JsonObject: Dictionary with a ``data`` list of providers.
        """
        response = await self.handler.request("providers")
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'providers' endpoint")
