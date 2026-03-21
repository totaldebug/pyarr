from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Artist(CommonActions):
    """Artist actions for Lidarr."""

    async def get(self, item_id: int | str | None = None, mb_id: str | None = None) -> JsonArray | JsonObject:
        """Returns artists by ID or MusicBrainz ID.

        Args:
            item_id (int | str | None, optional): Lidarr ID or MusicBrainz ID of artist. Defaults to None.
            mb_id (str | None, optional): MusicBrainz ID of artist. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        params = {}
        if mb_id:
            params["mbId"] = mb_id
        elif isinstance(item_id, str):
            params["mbId"] = item_id
            item_id = None

        return await self._get("artist", item_id=item_id, params=params)

    async def add(
        self,
        artist: JsonObject,
        root_dir: str,
        quality_profile_id: int,
        metadata_profile_id: int,
        monitored: bool = True,
        artist_monitor: str = "all",
        search_for_missing_albums: bool = False,
    ) -> JsonObject:
        """Adds an artist to the database.

        Args:
            artist (JsonObject): Artist record from `lookup()`.
            root_dir (str): Location of the root directory.
            quality_profile_id (int): ID of the quality profile.
            metadata_profile_id (int): ID of the metadata profile.
            monitored (bool, optional): Should the artist be monitored. Defaults to True.
            artist_monitor (str, optional): Monitor type. Defaults to "all".
            search_for_missing_albums (bool, optional): Search for missing albums. Defaults to False.

        Returns:
            JsonObject: Dictionary with added record.
        """
        artist["rootFolderPath"] = root_dir
        artist["qualityProfileId"] = quality_profile_id
        artist["metadataProfileId"] = metadata_profile_id
        artist["monitored"] = monitored
        artist["addOptions"] = {
            "monitor": artist_monitor,
            "searchForMissingAlbums": search_for_missing_albums,
        }

        response = await self.handler.request("artist", method="POST", json_data=artist)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'artist' endpoint")

    async def update(self, data: JsonObject) -> JsonObject:
        """Updates an artist in the database.

        Args:
            data (JsonObject): Dictionary containing artist data.

        Returns:
            JsonObject: Dictionary with updated record.
        """
        response = await self.handler.request("artist", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'artist' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete an artist by ID.

        Args:
            item_id (int): The ID of the artist to delete.
        """
        await self._delete("artist", item_id=item_id)

    async def lookup(self, term: str) -> JsonArray:
        """Search for an artist to add to the database.

        Args:
            term (str): Search term (can include lidarr: prefix for MusicBrainz ID).

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("artist/lookup", params={"term": term})
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'artist/lookup' endpoint")
