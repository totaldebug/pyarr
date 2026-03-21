from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class QualityProfile(CommonActions):
    """Quality profile actions for Arr clients."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of quality profiles or a specific profile by ID.

        Args:
            item_id (int | None, optional): ID of the quality profile to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("qualityprofile", item_id=item_id)

    async def get_schema(self) -> JsonArray | JsonObject:
        """Gets the schemas for quality profiles.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        response = await self.handler.request("qualityprofile/schema")
        if isinstance(response, list | dict):
            return response
        raise ValueError("Expected a list or dictionary response from the 'qualityprofile/schema' endpoint")

    async def add(self, data: JsonObject) -> JsonObject:
        """Add a new quality profile.

        Args:
            data (JsonObject): Dictionary with quality profile settings.

        Returns:
            JsonObject: Dictionary of added item.
        """
        response = await self.handler.request("qualityprofile", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'qualityprofile' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Edit a quality profile by database id.

        Args:
            item_id (int): Quality profile database id.
            data (JsonObject): Data to be updated within quality profile.

        Returns:
            JsonObject: Dictionary of updated item.
        """
        response = await self.handler.request(f"qualityprofile/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'qualityprofile/{item_id}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete a quality profile by ID.

        Args:
            item_id (int): The ID of the quality profile to delete.
        """
        await self._delete("qualityprofile", item_id=item_id)
