from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class ImportList(CommonActions):
    """Import list actions for Arr clients."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of import lists or a specific list by ID.

        Args:
            item_id (int | None, optional): ID of the import list to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("importlist", item_id=item_id)

    async def get_schema(self, implementation: str | None = None) -> JsonArray:
        """Gets the schemas for the different import lists.

        Args:
            implementation (str | None, optional): Client implementation name. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("importlist/schema")
        if not isinstance(response, list):
            raise ValueError("Expected a list response from the 'importlist/schema' endpoint")

        if implementation:
            return [item for item in response if item["implementation"] == implementation]
        return response

    async def add(self, data: JsonObject) -> JsonObject:
        """Add an import list.

        Args:
            data (JsonObject): Dictionary with import list schema and settings.

        Returns:
            JsonObject: Dictionary of added item.
        """
        response = await self.handler.request("importlist", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'importlist' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Edit an import list by database id.

        Args:
            item_id (int): Import list database id.
            data (JsonObject): Data to be updated within import list.

        Returns:
            JsonObject: Dictionary of updated item.
        """
        response = await self.handler.request(f"importlist/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'importlist/{item_id}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete an import list by ID.

        Args:
            item_id (int): The ID of the import list to delete.
        """
        await self._delete("importlist", item_id=item_id)
