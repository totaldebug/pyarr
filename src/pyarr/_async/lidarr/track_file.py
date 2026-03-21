from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class TrackFile(CommonActions):
    """Track file actions for Lidarr."""

    async def get(
        self,
        artist_id: int | None = None,
        album_id: int | None = None,
        track_file_ids: list[int] | None = None,
        unmapped: bool | None = None,
    ) -> JsonArray | JsonObject:
        """Returns track files based on IDs, or all unmapped files.

        Args:
            artist_id (int | None, optional): Artist database ID. Defaults to None.
            album_id (int | None, optional): Album database ID. Defaults to None.
            track_file_ids (list[int] | None, optional): Specific file IDs. Defaults to None.
            unmapped (bool | None, optional): Get all unmapped files. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        params: dict[str, int | list[int] | bool] = {}
        if artist_id:
            params["artistId"] = artist_id
        if album_id:
            params["albumId"] = album_id
        if track_file_ids:
            params["trackFileIds"] = track_file_ids
        if unmapped is not None:
            params["unmapped"] = unmapped

        item_id = None
        if track_file_ids and len(track_file_ids) == 1:
            item_id = track_file_ids[0]
            params.pop("trackFileIds")

        return await self._get("trackfile", item_id=item_id, params=params)

    async def update(self, data: JsonObject) -> JsonObject:
        """Update an existing track file.

        Args:
            data (JsonObject): Updated data for track files.

        Returns:
            JsonObject: Dictionary of updated record.
        """
        response = await self.handler.request("trackfile", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'trackfile' endpoint")

    async def delete(self, ids: int | list[int]) -> None:
        """Delete track files.

        Args:
            ids (int | list[int]): Single ID or list of IDs for files to delete.
        """
        if isinstance(ids, list):
            json_data = {"trackFileIds": ids}
            await self.handler.request("trackfile/bulk", method="DELETE", json_data=json_data)
        else:
            await self._delete("trackfile", item_id=ids)
