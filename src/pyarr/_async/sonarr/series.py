from pyarr._async.common.base import CommonActions
from pyarr.exceptions import PyarrMissingArgument
from pyarr.types import JsonArray, JsonObject


class Series(CommonActions):
    """Series actions for Sonarr."""

    async def get(self, item_id: int | None = None, tvdb: bool = False, tmdb: bool = False) -> JsonArray | JsonObject:
        """Returns the list of added series or a specific series by ID, TVDB ID, or TMDB ID.

        Args:
            item_id (int | None, optional): ID of the series to return. Defaults to None.
            tvdb (bool, optional): Set to true if item_id is the TVDB ID. Defaults to False.
            tmdb (bool, optional): Set to true if item_id is the TMDB ID. Defaults to False.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        if item_id and tvdb:
            params = {"tvdbid": item_id}
            response = await self.handler.request("series", params=params)
            if isinstance(response, list):
                return response
            raise ValueError(f"Expected a list response from the 'series?tvdbid={item_id}' endpoint")

        if item_id and tmdb:
            params = {"tmdbid": item_id}
            response = await self.handler.request("series", params=params)
            if isinstance(response, list):
                return response
            raise ValueError(f"Expected a list response from the 'series?tmdbid={item_id}' endpoint")

        return await self._get("series", item_id=item_id)

    async def add(
        self,
        series: JsonObject,
        quality_profile_id: int,
        language_profile_id: int,
        root_dir: str,
        season_folder: bool = True,
        monitored: bool = True,
        ignore_episodes_with_files: bool = False,
        ignore_episodes_without_files: bool = False,
        search_for_missing_episodes: bool = False,
    ) -> JsonObject:
        """Adds a new series to your collection.

        Args:
            series (JsonObject): A series object from `lookup()`.
            quality_profile_id (int): Database id for quality profile.
            language_profile_id (int): Database id for language profile.
            root_dir (str): Root folder location.
            season_folder (bool, optional): Create a folder for each season. Defaults to True.
            monitored (bool, optional): Monitor this series. Defaults to True.
            ignore_episodes_with_files (bool, optional): Ignore any episodes with existing files. Defaults to False.
            ignore_episodes_without_files (bool, optional): Ignore any episodes without existing files.
                Defaults to False.
            search_for_missing_episodes (bool, optional): Search for missing episodes to download. Defaults to False.

        Returns:
            JsonObject: Dictionary of added record.
        """
        if not monitored and series.get("seasons"):
            for season in series["seasons"]:
                season["monitored"] = False

        series["rootFolderPath"] = root_dir
        series["qualityProfileId"] = quality_profile_id
        series["languageProfileId"] = language_profile_id
        series["seasonFolder"] = season_folder
        series["monitored"] = monitored
        series["addOptions"] = {
            "ignoreEpisodesWithFiles": ignore_episodes_with_files,
            "ignoreEpisodesWithoutFiles": ignore_episodes_without_files,
            "searchForMissingEpisodes": search_for_missing_episodes,
        }
        response = await self.handler.request("series", method="POST", json_data=series)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'series' endpoint")

    async def update(self, data: JsonObject) -> JsonObject:
        """Updates a series in the database.

        Args:
            data (JsonObject): data to update series.

        Returns:
            JsonObject: updated series.
        """
        response = await self.handler.request("series", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'series' endpoint")

    async def delete(self, item_id: int, delete_files: bool = False) -> bool:
        """Delete a series from the database.

        Args:
            item_id (int): series id.
            delete_files (bool, optional): Also delete files associated with the series. Defaults to False.

        Returns:
            bool: True if series was deleted.
        """
        await self.handler.request(f"series/{item_id}", method="DELETE", params={"deleteFiles": delete_files})
        return True

    async def lookup(self, term: str | None = None, item_id: int | None = None) -> JsonArray:
        """Searches for new shows on TheTVDB.com.

        Args:
            term (Optional[str], optional): Series' Name.
            item_id (Optional[int], optional): TVDB ID for series.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        if term is None and item_id is None:
            raise PyarrMissingArgument("A term or TVDB id must be included")

        params = {"term": term or f"tvdb:{item_id}"}
        response = await self.handler.request("series/lookup", params=params)
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'series/lookup' endpoint")
