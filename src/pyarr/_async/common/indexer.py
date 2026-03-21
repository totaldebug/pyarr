from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Indexer(CommonActions):
    """Indexer actions for Arr clients."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of indexers or a specific indexer by ID.

        Args:
            item_id (int | None, optional): ID of the indexer to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("indexer", item_id=item_id)

    async def get_schema(self, implementation: str | None = None) -> JsonArray:
        """Gets the schemas for the different indexers.

        Args:
            implementation (str | None, optional): Indexer implementation name. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("indexer/schema")
        if not isinstance(response, list):
            raise ValueError("Expected a list response from the 'indexer/schema' endpoint")

        if implementation:
            return [item for item in response if item["implementation"] == implementation]
        return response

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Edit an indexer by database id.

        Args:
            item_id (int): Indexer database id.
            data (JsonObject): Data to be updated within indexer.

        Returns:
            JsonObject: Dictionary of updated record.
        """
        response = await self.handler.request(f"indexer/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'indexer/{item_id}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete an indexer by ID.

        Args:
            item_id (int): The ID of the indexer to delete.
        """
        await self._delete("indexer", item_id=item_id)
