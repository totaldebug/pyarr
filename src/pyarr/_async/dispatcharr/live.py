from pyarr._async.common.base import CommonActions
from pyarr.types import JsonObject


class Live(CommonActions):
    """Live actions for Dispatcharr."""

    async def get_stream(self, username: str, password: str, channel_id: str) -> JsonObject:
        """Retrieve live stream.

        Args:
            username (str): Username.
            password (str): Password.
            channel_id (str): Channel ID.

        Returns:
            JsonObject: The response data.
        """
        # This hits /{username}/{password}/{channel_id}
        # Since api_url is base_url/api/, we need to go up one level
        return await self.handler.request(f"../{username}/{password}/{channel_id}", method="GET")

    async def get_live_stream(self, username: str, password: str, channel_id: str) -> JsonObject:
        """Retrieve live stream via /live endpoint.

        Args:
            username (str): Username.
            password (str): Password.
            channel_id (str): Channel ID.

        Returns:
            JsonObject: The response data.
        """
        # This hits /live/{username}/{password}/{channel_id}
        return await self.handler.request(f"../live/{username}/{password}/{channel_id}", method="GET")
