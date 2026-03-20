from pyarr.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class QualityProfile(CommonActions):
    """Quality profile actions for Arr clients."""

    def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of quality profiles or a specific profile by ID.

        Args:
            item_id (int | None, optional): ID of the quality profile to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return self._get("qualityprofile", item_id=item_id)

    def get_schema(self) -> JsonArray | JsonObject:
        """Gets the schemas for quality profiles.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        response = self.handler.request("qualityprofile/schema")
        if isinstance(response, list | dict):
            return response
        raise ValueError("Expected a list or dictionary response from the 'qualityprofile/schema' endpoint")

    def add(self, data: JsonObject) -> JsonObject:
        """Add a new quality profile.

        Args:
            data (JsonObject): Dictionary with quality profile settings.

        Returns:
            JsonObject: Dictionary of added item.
        """
        response = self.handler.request("qualityprofile", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'qualityprofile' endpoint")

    def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Edit a quality profile by database id.

        Args:
            item_id (int): Quality profile database id.
            data (JsonObject): Data to be updated within quality profile.

        Returns:
            JsonObject: Dictionary of updated item.
        """
        response = self.handler.request(f"qualityprofile/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'qualityprofile/{item_id}' endpoint")

    def delete(self, item_id: int) -> None:
        """Delete a quality profile by ID.

        Args:
            item_id (int): The ID of the quality profile to delete.
        """
        self._delete("qualityprofile", item_id=item_id)
