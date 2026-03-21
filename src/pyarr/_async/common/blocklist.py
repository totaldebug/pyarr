from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Blocklist(CommonActions):
    """Blocklist actions for Arr clients."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of blocklists or a specific blocklist by ID.

        Args:
            item_id (int | None, optional): ID of the blocklist to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("blocklist", item_id=item_id)

    async def delete(self, item_id: int) -> None:
        """Delete a blocklist by its database id.

        Args:
            item_id (int): Database id of blocklist.
        """
        await self._delete("blocklist", item_id=item_id)

    async def bulk_delete(self, item_ids: list[int]) -> None:
        """Delete blocklists in bulk.

        Args:
            item_ids (list[int]): List of blocklist IDs.
        """
        json_data = {"ids": item_ids}
        await self.handler.request("blocklist/bulk", method="DELETE", json_data=json_data)
