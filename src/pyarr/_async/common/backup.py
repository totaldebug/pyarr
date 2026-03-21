from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Backup(CommonActions):
    """Backup actions for Arr clients."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of available backups or a specific backup by ID.

        Args:
            item_id (int | None, optional): ID of the backup to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        return await self._get("system/backup", item_id=item_id)

    async def delete(self, item_id: int) -> JsonObject:
        """Delete a backup by ID.

        Args:
            item_id (int): The ID of the backup to delete.

        Returns:
            JsonObject: The response data.
        """
        response = await self._delete("system/backup", item_id=item_id)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'system/backup/{item_id}' endpoint")

    async def create(self) -> JsonObject:
        """Creates a backup.

        Returns:
            JsonObject: An item including the backup information.
        """
        endpoint = "command"
        json_data = {"name": "Backup"}
        response = await self.handler.request(endpoint, method="POST", json_data=json_data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the '{endpoint}' endpoint")

    # TODO: Restore Backup
