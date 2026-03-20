from pyarr.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Channels(CommonActions):
    """Channel actions for Dispatcharr."""

    def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of channels or a specific channel by ID.

        Args:
            item_id (int | None, optional): ID of the channel to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return self._get("channels", item_id=item_id)

    def add(self, data: JsonObject) -> JsonObject:
        """Add a new channel.

        Args:
            data (JsonObject): Channel configuration.

        Returns:
            JsonObject: Added channel details.
        """
        response = self.handler.request("channels", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'channels' endpoint")

    def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an existing channel.

        Args:
            item_id (int): Channel ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated channel details.
        """
        response = self.handler.request(f"channels/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'channels/{item_id}' endpoint")

    def delete(self, item_id: int) -> None:
        """Delete a channel.

        Args:
            item_id (int): Channel ID.
        """
        self._delete("channels", item_id=item_id)
