from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class QualityDefinition(CommonActions):
    """Quality definition actions for Arr clients."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of quality definitions or a specific definition by ID.

        Args:
            item_id (int | None, optional): ID of the quality definition to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("qualitydefinition", item_id=item_id)

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Edit a quality definition by database id.

        Args:
            item_id (int): Quality definition database id.
            data (JsonObject): Data to be updated within quality definition.

        Returns:
            JsonObject: Dictionary of updated item.
        """
        response = await self.handler.request(f"qualitydefinition/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'qualitydefinition/{item_id}' endpoint")
