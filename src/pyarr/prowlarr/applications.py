from pyarr.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Applications(CommonActions):
    """Application management actions for Prowlarr."""

    def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of connected applications or a specific application by ID.

        Args:
            item_id (int | None, optional): ID of the application to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return self._get("applications", item_id=item_id)

    def test(self, data: JsonObject) -> JsonObject:
        """Test connection to an application.

        Args:
            data (JsonObject): Application configuration to test.

        Returns:
            JsonObject: Test results.
        """
        response = self.handler.request("applications/test", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'applications/test' endpoint")

    def add(self, data: JsonObject) -> JsonObject:
        """Add a new application.

        Args:
            data (JsonObject): Application configuration.

        Returns:
            JsonObject: Added application details.
        """
        response = self.handler.request("applications", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'applications' endpoint")

    def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an existing application.

        Args:
            item_id (int): Application ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated application details.
        """
        response = self.handler.request(f"applications/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'applications/{item_id}' endpoint")

    def delete(self, item_id: int) -> None:
        """Delete an application.

        Args:
            item_id (int): Application ID.
        """
        self._delete("applications", item_id=item_id)
