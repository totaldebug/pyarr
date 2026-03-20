from pyarr.common.base import CommonActions
from pyarr.types import JsonArray


class Release(CommonActions):
    """Release actions for Lidarr."""

    def get(self, artist_id: int | None = None, album_id: int | None = None) -> JsonArray:
        """Search indexers for specified fields.

        Args:
            artist_id (int | None, optional): Artist ID from DB. Defaults to None.
            album_id (int | None, optional): Album ID from DB. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        params = {}
        if artist_id:
            params["artistId"] = artist_id
        if album_id:
            params["albumId"] = album_id

        response = self.handler.request("release", params=params)
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'release' endpoint")
