from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class ChannelLogos(CommonActions):
    """Channel logo actions for Dispatcharr."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve channel logos.

        Args:
            item_id (int | None, optional): ID of the logo to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("channels/logos/", item_id=item_id)

    async def add(self, data: JsonObject) -> JsonObject:
        """Create a new logo entry.

        Args:
            data (JsonObject): Logo data.

        Returns:
            JsonObject: Added logo details.
        """
        response = await self.handler.request("channels/logos/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'channels/logos/' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an existing logo.

        Args:
            item_id (int): Logo ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated logo details.
        """
        response = await self.handler.request(f"channels/logos/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/logos/{item_id}/' endpoint")

    async def partial_update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update an existing logo.

        Args:
            item_id (int): Logo ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated logo details.
        """
        response = await self.handler.request(f"channels/logos/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/logos/{item_id}/' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete a logo.

        Args:
            item_id (int): Logo ID.
        """
        await self._delete("channels/logos/", item_id=item_id)

    async def get_cache(self, item_id: int) -> JsonObject:
        """Retrieve cached logo.

        Args:
            item_id (int): Logo ID.

        Returns:
            JsonObject: The response data.
        """
        return await self._get(f"channels/logos/{item_id}/cache/")

    async def bulk_delete(self, ids: list[int]) -> None:
        """Bulk delete logos by ID.

        Args:
            ids (list[int]): List of logo IDs.
        """
        await self.handler.request("channels/logos/bulk-delete/", method="DELETE", json_data={"ids": ids})

    async def cleanup(self, data: JsonObject) -> None:
        """Delete all channel logos that are not used.

        Args:
            data (JsonObject): Cleanup request data.
        """
        await self.handler.request("channels/logos/cleanup/", method="POST", json_data=data)

    async def upload(self, data: JsonObject) -> JsonObject:
        """Upload a logo.

        Args:
            data (JsonObject): Logo file data.

        Returns:
            JsonObject: Added logo details.
        """
        response = await self.handler.request("channels/logos/upload/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'channels/logos/upload/' endpoint")
