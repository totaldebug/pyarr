from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class DownloadClient(CommonActions):
    """Download client actions for Arr clients."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of download clients or a specific client by ID.

        Args:
            item_id (int | None, optional): ID of the download client to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("downloadclient", item_id=item_id)

    async def get_schema(self, implementation: str | None = None) -> JsonArray:
        """Gets the schemas for the different download clients.

        Args:
            implementation (str | None, optional): Client implementation name. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("downloadclient/schema")
        if not isinstance(response, list):
            raise ValueError("Expected a list response from the 'downloadclient/schema' endpoint")

        if implementation:
            return [item for item in response if item["implementation"] == implementation]
        return response

    async def add(self, data: JsonObject) -> JsonObject:
        """Add a download client.

        Args:
            data (JsonObject): Dictionary with download client schema and settings.

        Returns:
            JsonObject: Dictionary of added item.
        """
        response = await self.handler.request("downloadclient", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'downloadclient' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Edit a download client by database id.

        Args:
            item_id (int): Download client database id.
            data (JsonObject): Data to be updated within download client.

        Returns:
            JsonObject: Dictionary of updated item.
        """
        response = await self.handler.request(f"downloadclient/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'downloadclient/{item_id}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete a download client by ID.

        Args:
            item_id (int): The ID of the download client to delete.
        """
        await self._delete("downloadclient", item_id=item_id)
