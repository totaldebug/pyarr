from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Notification(CommonActions):
    """Notification actions for Arr clients."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of notification services or a specific service by ID.

        Args:
            item_id (int | None, optional): ID of the notification to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("notification", item_id=item_id)

    async def get_schema(self, implementation: str | None = None) -> JsonArray:
        """Gets the schemas for the different notification services.

        Args:
            implementation (str | None, optional): Notification implementation name. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("notification/schema")
        if not isinstance(response, list):
            raise ValueError("Expected a list response from the 'notification/schema' endpoint")

        if implementation:
            return [item for item in response if item["implementation"] == implementation]
        return response

    async def add(self, data: JsonObject) -> JsonObject:
        """Add a notification service.

        Args:
            data (JsonObject): Dictionary with notification schema and settings.

        Returns:
            JsonObject: Dictionary of added item.
        """
        response = await self.handler.request("notification", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'notification' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Edit a notification service by database id.

        Args:
            item_id (int): Notification database id.
            data (JsonObject): Data to be updated within notification.

        Returns:
            JsonObject: Dictionary of updated item.
        """
        response = await self.handler.request(f"notification/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'notification/{item_id}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete a notification service by ID.

        Args:
            item_id (int): The ID of the notification to delete.
        """
        await self._delete("notification", item_id=item_id)
