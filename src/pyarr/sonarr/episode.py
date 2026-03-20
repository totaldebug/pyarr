from pyarr.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Episode(CommonActions):
    """Episode actions for Sonarr."""

    def get(self, item_id: int | None = None, series_id: int | None = None) -> JsonArray | JsonObject:
        """Returns episodes by ID or series ID.

        Args:
            item_id (int | None, optional): ID for Episode. Defaults to None.
            series_id (int | None, optional): ID for Series. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        params = {}
        if series_id:
            params["seriesId"] = series_id

        return self._get("episode", item_id=item_id, params=params)

    def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update the given episode.

        Args:
            item_id (int): ID of the Episode to be updated.
            data (JsonObject): Parameters to update the episode.

        Returns:
            JsonObject: Dictionary with updated record.
        """
        response = self.handler.request(f"episode/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'episode/{item_id}' endpoint")

    def monitor(self, episode_ids: list[int], monitored: bool = True) -> JsonArray:
        """Update episode monitored status.

        Args:
            episode_ids (list[int]): All episode IDs to be updated.
            monitored (bool, optional): True or False. Defaults to True.

        Returns:
            JsonArray: list of dictionaries containing updated records.
        """
        json_data = {"episodeIds": episode_ids, "monitored": monitored}
        response = self.handler.request("episode/monitor", method="PUT", json_data=json_data)
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'episode/monitor' endpoint")
