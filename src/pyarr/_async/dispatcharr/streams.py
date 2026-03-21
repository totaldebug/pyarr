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
        return await self._get("streams", item_id=item_id)

    async def add(self, data: JsonObject) -> JsonObject:
        """Add a new stream.

        Args:
            data (JsonObject): Stream configuration.

        Returns:
            JsonObject: Added stream details.
        """
        response = await self.handler.request("streams", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'streams' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an existing stream.

        Args:
            item_id (int): Stream ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated stream details.
        """
        response = await self.handler.request(f"streams/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'streams/{item_id}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete a stream.

        Args:
            item_id (int): Stream ID.
        """
        await self._delete("streams", item_id=item_id)
