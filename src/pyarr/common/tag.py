from typing import Any

from pyarr.common.base import CommonActions
from pyarr.types import JsonObject


class Tag(CommonActions):
    """Tag actions for Arr clients."""

    def get(self, item_id: int | None = None) -> Any:
        """Returns the list of added tags or a specific tag by ID.

        Args:
            item_id (int | None, optional): ID of the tag to return. Defaults to None.

        Returns:
            Any: List of dictionaries with items or a single dictionary.
        """
        return self._get("tag", item_id=item_id)

    def get_detail(self, item_id: int | None = None) -> Any:
        """Returns detailed information about a specific tag or all tags.

        Args:
            item_id (int | None, optional): ID of the tag to return. Defaults to None.

        Returns:
            Any: List of dictionaries with items or a single dictionary.
        """
        return self._get("tag/detail", item_id=item_id)

    def create(self, label: str) -> JsonObject:
        """Adds a new tag.

        Args:
            label (str): Tag name / label.

        Returns:
            JsonObject: Dictionary of added item.
        """
        response = self.handler.request("tag", method="POST", json_data={"label": label})
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'tag' endpoint")

    def update(self, item_id: int, label: str) -> JsonObject:
        """Updates a tag by database id.

        Args:
            item_id (int): Database id of tag.
            label (str): New label for the tag.

        Returns:
            JsonObject: Dictionary of updated item.
        """
        response = self.handler.request("tag", method="PUT", json_data={"id": item_id, "label": label})
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'tag' endpoint")

    def delete(self, item_id: int) -> None:
        """Delete a tag by its database id.

        Args:
            item_id (int): Database id of tag.
        """
        self._delete("tag", item_id=item_id)
