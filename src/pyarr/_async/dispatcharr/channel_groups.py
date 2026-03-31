from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class ChannelGroups(CommonActions):
    """Channel group actions for Dispatcharr."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve channel groups.

        Args:
            item_id (int | None, optional): ID of the group to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("channels/groups/", item_id=item_id)

    async def add(self, data: JsonObject) -> JsonObject:
        """Create a new channel group.

        Args:
            data (JsonObject): Group data.

        Returns:
            JsonObject: Added group details.
        """
        response = await self.handler.request("channels/groups/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'channels/groups/' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update a channel group.

        Args:
            item_id (int): Group ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated group details.
        """
        response = await self.handler.request(f"channels/groups/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/groups/{item_id}/' endpoint")

    async def partial_update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update a channel group.

        Args:
            item_id (int): Group ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated group details.
        """
        response = await self.handler.request(f"channels/groups/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/groups/{item_id}/' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete a channel group.

        Args:
            item_id (int): Group ID.
        """
        await self._delete("channels/groups/", item_id=item_id)

    async def cleanup(self, data: JsonObject) -> JsonObject:
        """Delete all channel groups that have no associations.

        Args:
            data (JsonObject): Cleanup request data.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("channels/groups/cleanup/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'channels/groups/cleanup/' endpoint")
