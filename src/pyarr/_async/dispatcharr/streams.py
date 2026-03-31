from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Streams(CommonActions):
    """Stream actions for Dispatcharr."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of streams or a specific stream by ID.

        Args:
            item_id (int | None, optional): ID of the stream to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("channels/streams/", item_id=item_id)

    async def add(self, data: JsonObject) -> JsonObject:
        """Add a new stream.

        Args:
            data (JsonObject): Stream configuration.

        Returns:
            JsonObject: Added stream details.
        """
        response = await self.handler.request("channels/streams/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'channels/streams/' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an existing stream.

        Args:
            item_id (int): Stream ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated stream details.
        """
        response = await self.handler.request(f"channels/streams/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/streams/{item_id}/' endpoint")

    async def partial_update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update an existing stream.

        Args:
            item_id (int): Stream ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated stream details.
        """
        response = await self.handler.request(f"channels/streams/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/streams/{item_id}/' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete a stream.

        Args:
            item_id (int): Stream ID.
        """
        await self._delete("channels/streams/", item_id=item_id)

    async def bulk_delete(self, ids: list[int]) -> None:
        """Bulk delete streams by ID.

        Args:
            ids (list[int]): List of stream IDs.
        """
        await self.handler.request("channels/streams/bulk-delete/", method="DELETE", json_data={"ids": ids})

    async def get_by_ids(self, ids: list[int]) -> JsonArray | JsonObject:
        """Retrieve streams by a list of IDs.

        Args:
            ids (list[int]): List of stream IDs.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        response = await self.handler.request("channels/streams/by-ids/", method="POST", json_data={"ids": ids})
        return response

    async def get_filter_options(self) -> JsonObject:
        """Retrieve filter options for streams.

        Returns:
            JsonObject: The response data.
        """
        return await self._get("channels/streams/filter-options/")

    async def get_groups(self) -> JsonArray | JsonObject:
        """Retrieve stream groups.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("channels/streams/groups/")

    async def get_ids(self) -> JsonArray | JsonObject:
        """Retrieve all stream IDs.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("channels/streams/ids/")
