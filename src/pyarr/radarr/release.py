from datetime import datetime

from pyarr.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Release(CommonActions):
    """Release actions for Radarr."""

    def get(self, movie_id: int | None = None) -> JsonArray:
        """Query indexers for latest releases.

        Args:
            movie_id (int | None, optional): Database id for movie to check. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        params = {}
        if movie_id:
            params["movieId"] = movie_id

        response = self.handler.request("release", params=params)
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'release' endpoint")

    def add(self, guid: str, indexer_id: int) -> JsonObject:
        """Adds a previously searched release to the download client.

        Args:
            guid (str): Recently searched result guid.
            indexer_id (int): Database id of indexer to use.

        Returns:
            JsonObject: Dictionary with download release details.
        """
        json_data = {"guid": guid, "indexerId": indexer_id}
        response = self.handler.request("release", method="POST", json_data=json_data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'release' endpoint")

    def push(self, title: str, download_url: str, protocol: str, publish_date: datetime) -> JsonArray:
        """If the title is wanted, Radarr will grab it.

        Args:
            title (str): Release name.
            download_url (str): .torrent file URL.
            protocol (str): "Usenet" or "Torrent".
            publish_date (datetime): ISO8601 date.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        json_data = {
            "title": title,
            "downloadUrl": download_url,
            "protocol": protocol,
            "publishDate": publish_date.isoformat(),
        }
        response = self.handler.request("release/push", method="POST", json_data=json_data)
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'release/push' endpoint")
