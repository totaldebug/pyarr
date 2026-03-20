from pyarr.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Track(CommonActions):
    """Track actions for Lidarr."""

    def get(
        self,
        artist_id: int | None = None,
        album_id: int | None = None,
        album_release_id: int | None = None,
        track_ids: list[int] | None = None,
    ) -> JsonArray | JsonObject:
        """Returns tracks based on provided IDs.

        Args:
            artist_id (int | None, optional): Artist ID. Defaults to None.
            album_id (int | None, optional): Album ID. Defaults to None.
            album_release_id (int | None, optional): Album Release ID. Defaults to None.
            track_ids (list[int] | None, optional): Track IDs. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        params: dict[str, int | list[int]] = {}
        if artist_id:
            params["artistId"] = artist_id
        if album_id:
            params["albumId"] = album_id
        if album_release_id:
            params["albumReleaseId"] = album_release_id
        if track_ids:
            params["trackIds"] = track_ids

        # If track_ids is a single int, it might be used in the path
        item_id = None
        if track_ids and len(track_ids) == 1:
            item_id = track_ids[0]
            params.pop("trackIds")

        return self._get("track", item_id=item_id, params=params)
