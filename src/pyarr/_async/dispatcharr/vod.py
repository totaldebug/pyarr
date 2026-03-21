from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Vod(CommonActions):
    """VOD actions for Dispatcharr."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of VOD content or a specific item by ID.

        Args:
            item_id (int | None, optional): ID of the VOD item to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("vod", item_id=item_id)

    async def add(self, data: JsonObject) -> JsonObject:
        """Add a new VOD item.

        Args:
            data (JsonObject): VOD configuration.

        Returns:
            JsonObject: Added VOD details.
        """
        response = await self.handler.request("vod", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'vod' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an existing VOD item.

        Args:
            item_id (int): VOD ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated VOD details.
        """
        response = await self.handler.request(f"vod/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'vod/{item_id}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete a VOD item.

        Args:
            item_id (int): VOD ID.
        """
        await self._delete("vod", item_id=item_id)
