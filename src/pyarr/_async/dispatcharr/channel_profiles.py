from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class ChannelProfiles(CommonActions):
    """Channel profile actions for Dispatcharr."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve channel profiles.

        Args:
            item_id (int | None, optional): ID of the profile to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("channels/profiles", item_id=item_id)

    async def add(self, data: JsonObject) -> JsonObject:
        """Create a new channel profile.

        Args:
            data (JsonObject): Profile data.

        Returns:
            JsonObject: Added profile details.
        """
        response = await self.handler.request("channels/profiles", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'channels/profiles' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update a channel profile.

        Args:
            item_id (int): Profile ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated profile details.
        """
        response = await self.handler.request(f"channels/profiles/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/profiles/{item_id}' endpoint")

    async def partial_update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update a channel profile.

        Args:
            item_id (int): Profile ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated profile details.
        """
        response = await self.handler.request(f"channels/profiles/{item_id}", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/profiles/{item_id}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete a channel profile.

        Args:
            item_id (int): Profile ID.
        """
        await self._delete("channels/profiles", item_id=item_id)

    async def duplicate(self, item_id: int) -> JsonObject:
        """Duplicate a channel profile.

        Args:
            item_id (int): Profile ID.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request(f"channels/profiles/{item_id}/duplicate", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/profiles/{item_id}/duplicate' endpoint")

    async def partial_update_channels(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update channels in a profile.

        Args:
            item_id (int): Profile ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated profile details.
        """
        response = await self.handler.request(f"channels/profiles/{item_id}/channels", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/profiles/{item_id}/channels' endpoint")

    async def bulk_update_channels(self, item_id: int, data: JsonObject) -> JsonObject:
        """Bulk update channels in a profile.

        Args:
            item_id (int): Profile ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated profile details.
        """
        response = await self.handler.request(
            f"channels/profiles/{item_id}/channels/bulk-update",
            method="PATCH",
            json_data=data,
        )
        if isinstance(response, dict):
            return response
        raise ValueError(
            f"Expected a dictionary response from the 'channels/profiles/{item_id}/channels/bulk-update' endpoint"
        )
