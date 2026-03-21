from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class IndexerProxy(CommonActions):
    """Indexer proxy actions for Prowlarr."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of indexer proxies or a specific proxy by ID.

        Args:
            item_id (int | None, optional): ID of the proxy to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("indexerproxy", item_id=item_id)

    async def add(self, data: JsonObject) -> JsonObject:
        """Add a new indexer proxy.

        Args:
            data (JsonObject): Proxy configuration.

        Returns:
            JsonObject: Added proxy details.
        """
        response = await self.handler.request("indexerproxy", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'indexerproxy' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an existing indexer proxy.

        Args:
            item_id (int): Proxy ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated proxy details.
        """
        response = await self.handler.request(f"indexerproxy/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'indexerproxy/{item_id}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete an indexer proxy.

        Args:
            item_id (int): Proxy ID.
        """
        await self._delete("indexerproxy", item_id=item_id)
