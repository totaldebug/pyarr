from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Movie(CommonActions):
    """Movie actions for Radarr."""

    async def get(self, item_id: int | None = None, tmdb_id: int | None = None) -> JsonArray | JsonObject:
        """Returns movies by ID or TMDB ID.

        Args:
            item_id (int | None, optional): Radarr ID of movie. Defaults to None.
            tmdb_id (int | None, optional): TMDB ID of movie. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        params = {}
        if tmdb_id:
            params["tmdbid"] = tmdb_id

        return await self._get("movie", item_id=item_id, params=params)

    async def add(
        self,
        movie: JsonObject,
        root_dir: str,
        quality_profile_id: int,
        monitored: bool = True,
        search_for_movie: bool = True,
        monitor: str = "movieOnly",
        minimum_availability: str = "announced",
        tags: list[int] | None = None,
    ) -> JsonObject:
        """Adds a movie to the database.

        Args:
            movie (JsonObject): Movie record from `lookup()`.
            root_dir (str): Location of the root directory.
            quality_profile_id (int): ID of the quality profile.
            monitored (bool, optional): Should the movie be monitored. Defaults to True.
            search_for_movie (bool, optional): Should we search for the movie. Defaults to True.
            monitor (str, optional): Monitor movie or collection. Defaults to "movieOnly".
            minimum_availability (str, optional): Availability of movie. Defaults to "announced".
            tags (list[int], optional): List of tag IDs. Defaults to None.

        Returns:
            JsonObject: Dictionary with added record.
        """
        movie["rootFolderPath"] = root_dir
        movie["qualityProfileId"] = quality_profile_id
        movie["monitored"] = monitored
        movie["minimumAvailability"] = minimum_availability
        movie["addOptions"] = {
            "monitor": monitor,
            "searchForMovie": search_for_movie,
        }
        if tags:
            movie["tags"] = tags

        response = await self.handler.request("movie", method="POST", json_data=movie)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'movie' endpoint")

    async def update(self, data: JsonObject, move_files: bool | None = None) -> JsonObject:
        """Updates a movie in the database.

        Args:
            data (JsonObject): Dictionary containing movie data.
            move_files (bool | None, optional): Have radarr move files when updating. Defaults to None.

        Returns:
            JsonObject: Dictionary with updated record.
        """
        params = {}
        if move_files is not None:
            params["moveFiles"] = move_files

        response = await self.handler.request("movie", method="PUT", json_data=data, params=params)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'movie' endpoint")

    async def delete(
        self,
        item_id: int | list[int],
        delete_files: bool = False,
        add_exclusion: bool = False,
    ) -> None:
        """Delete a single movie or multiple movies.

        Args:
            item_id (int | list[int]): Single ID or list of IDs to delete.
            delete_files (bool, optional): Delete movie files. Defaults to False.
            add_exclusion (bool, optional): Add to List Exclusions. Defaults to False.
        """
        params: dict[str, bool] = {
            "deleteFiles": delete_files,
            "addImportExclusion": add_exclusion,
        }

        if isinstance(item_id, list):
            json_data = {"movieIds": item_id}
            await self.handler.request("movie/editor", method="DELETE", json_data=json_data, params=params)
        else:
            await self.handler.request(f"movie/{item_id}", method="DELETE", params=params)

    async def lookup(self, term: str) -> JsonArray:
        """Search for a movie to add to the database.

        Args:
            term (str): Search term (can include imdb: or tmdb: prefixes).

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("movie/lookup", params={"term": term})
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'movie/lookup' endpoint")
