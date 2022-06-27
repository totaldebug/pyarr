from datetime import datetime
from typing import Any, Optional
from warnings import warn

from requests import Response

from .base import BaseArrAPI
from .const import PAGE, PAGE_SIZE
from .models.common import PyarrSortDirection
from .models.sonarr import SonarrCommands, SonarrSortKeys


class SonarrAPI(BaseArrAPI):
    """API wrapper for Sonarr endpoints."""

    def __init__(self, host_url: str, api_key: str, ver_uri: str = "/v3"):
        """Initialize the Sonarr API.

        Args:
            host_url (str): URL for Sonarr
            api_key (str): API key for Sonarr
            ver_uri (str): Version URI for Radarr. Defaults to None (empty string).
        """

        super().__init__(host_url, api_key, ver_uri)

    def _series_json(
        self,
        tvdb_id: int,
        quality_profile_id: int,
        root_dir: str,
        season_folder: bool = True,
        monitored: bool = True,
        ignore_episodes_with_files: bool = False,
        ignore_episodes_without_files: bool = False,
        search_for_missing_episodes: bool = False,
    ) -> dict:
        """Searches for new shows on trakt and returns Series JSON to add

        Args:
            tvdb_id (int): TVDB id to search
            quality_profile_id (int): Database id for Quality profile
            root_dir (str): Root directory for media
            season_folder (bool, optional): Specify if a season folder should be created. Defaults to True.
            monitored (bool, optional): Specify if the series should be monitored. Defaults to True.
            ignore_episodes_with_files (bool, optional): Ignore episodes that already have files. Defaults to False.
            ignore_episodes_without_files (bool, optional): Ignore episodes that dont have any files. Defaults to False.
            search_for_missing_episodes (bool, optional): Search for any missing episodes and download them. Defaults to False.

        Returns:
            dict: dictionary of series data
        """
        series = self.lookup_series_by_tvdb_id(tvdb_id)[0]
        if not monitored and series.get("seasons"):
            for season in series["seasons"]:
                season["monitored"] = False

        return {
            "title": series["title"],
            "seasons": series["seasons"],
            "rootFolderPath": root_dir,
            "qualityProfileId": quality_profile_id,
            "seasonFolder": season_folder,
            "monitored": monitored,
            "tvdbId": tvdb_id,
            "images": series["images"],
            "titleSlug": series["titleSlug"],
            "addOptions": {
                "ignoreEpisodesWithFiles": ignore_episodes_with_files,
                "ignoreEpisodesWithoutFiles": ignore_episodes_without_files,
                "searchForMissingEpisodes": search_for_missing_episodes,
            },
        }

    ## COMMAND

    # GET /command
    def get_command(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Queries the status of a previously started command, or all currently started commands.

        Args:
            id_ (Optional[int], optional): Database ID of the command. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"command/{id_}" if id_ else "command"
        return self.assert_return(path, self.ver_uri, list)

    # POST /command
    # TODO: confirm response, kwargs
    def post_command(self, name: SonarrCommands, **kwargs) -> Any:
        """Performs any of the predetermined Sonarr command routines

        Note:
            For additional kwargs:
            See https://github.com/Sonarr/Sonarr/wiki/Command

        Args:
            name (SonarrCommands): command name that should be execured
            **kwargs: additional parameters for specific commands



        Returns:
            JSON: Array
        """
        data = {
            "name": name,
            **kwargs,
        }
        return self._post("command", self.ver_uri, data=data)

    ## EPISODE

    # GET /episode
    def get_episode(self, id_: int, series: bool = False) -> dict[str, Any]:
        """Get get episodes by ID or series

        Args:
            id_ (int): ID for Episode or Series.
            series (bool, optional): Set to true if the ID is for a Series. Defaults to false.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return(
            f"episode{'' if series else f'/{id_}'}",
            self.ver_uri,
            dict,
            params={"seriesId": id_} if series else None,
        )

    # GET /episode
    def get_episodes_by_series_id(self, id_: int) -> list[dict[str, Any]]:
        # sourcery skip: class-extract-method
        """Gets all episodes from a given series ID

        Args:
            id_ (int): Database id for series

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. Please use get_episode()",
            DeprecationWarning,
            stacklevel=2,
        )
        params = {"seriesId": id_}
        return self.assert_return("episode", self.ver_uri, list, params)

    # GET /episode/{id}
    def get_episode_by_episode_id(self, id_: int) -> dict[str, Any]:
        """Gets a specific episode by database id

        Args:
            id_ (int): Database id for episode

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. Please use get_episode()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.assert_return(f"episode/{id_}", self.ver_uri, dict)

    # PUT /episode
    def upd_episode(self, id_: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update the given episodes, currently only monitored is supported

        Args:
            id_ (int): ID of the Episode to be updated
            data (dict[str, Any]): Parameters to update the episode

        Example:
            ::
                payload = {"monitored": True}
                sonarr.upd_episode(1, payload)

        Returns:
            dict[str, Any]: Dictionary with updated record
        """
        return self._put(f"episode/{id_}", self.ver_uri, data=data)

    ## EPISODE FILE

    # GET /episodefile
    def get_episode_files_by_series_id(self, id_: int) -> list[dict[str, Any]]:
        """Returns all episode file information for series id specified

        Args:
            id_ (int): Database id of series

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {"seriesId": id_}
        return self.assert_return("episodefile", self.ver_uri, list, params)

    # GET /episodefile/{id}
    def get_episode_file(self, id_: int) -> list[dict[str, Any]]:
        """Returns episode file information for specified id

        Args:
            id_ (int): Database id of episode file

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return(f"episodefile/{id_}", self.ver_uri, list)

    # DELETE /episodefile/{id}
    def del_episode_file(self, id_: int) -> Response:
        """Deletes the episode file with corresponding id

        Args:
            id_ (int): Database id for episode file

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"episodefile/{id_}", self.ver_uri)

    # PUT /episodefile/{id}
    def upd_episode_file_quality(
        self, id_: int, data: dict[str, Any]
    ) -> dict[str, Any]:
        """Updates the quality of the episode file and returns the episode file

        Args:
            id_ (int): Database id for episode file
            data (dict[str, Any]): data with quality::

                {
                    "quality": {
                        "quality": {
                        "id": 8
                        },
                        "revision": {
                        "version": 1,
                        "real": 0
                        }
                    },
                }

        Returns:
            dict[str, Any]: Dictionary with updated record
        """
        return self._put(f"episodefile/{id_}", self.ver_uri, data=data)

    # GET /wanted/missing
    def get_wanted(
        self,
        sort_key: SonarrSortKeys = SonarrSortKeys.AIR_DATE_UTC,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_dir: PyarrSortDirection = PyarrSortDirection.ASC,
    ) -> dict[str, Any]:
        """Gets missing episode (episodes without files)

        Args:
            sort_key (SonarrSortKeys, optional): series.titke or airDateUtc. Defaults to SonarrSortKeys.AIR_DATE_UTC.
            page (int, optional): Page number to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_dir (PyarrSortDirection, optional): Direction to sort the items. Defaults to PyarrSortDirection.ASC.

        Returns:
            dict[str, Any]: Dictionary with items
        """
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDir": sort_dir,
        }
        return self.assert_return("wanted/missing", self.ver_uri, dict, params)

    # PROFILES

    # GET /profile/{id}
    def get_quality_profile(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Gets all quality profiles or specific one with id_

        Args:
            id_ (int): quality profile id from database

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"profile/{id_}" if id_ else "profile"
        return self.assert_return(path, self.ver_uri, list)

    ## QUEUE

    # GET /queue
    def get_queue(self) -> list[dict[str, Any]]:
        """Gets currently downloading info

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("queue", self.ver_uri, list)

    ## PARSE

    # GET /parse
    def get_parsed_title(self, title: str) -> list[dict[str, Any]]:
        """Returns the result of parsing a title. series and episodes will be
        returned only if the parsing matches to a specific series and one or more
        episodes. series and episodes will be formatted the same as Series and Episode
        responses.

        Args:
            title (str): Title of series / episode

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("parse", self.ver_uri, list, {"title": title})

    # GET /parse
    def get_parsed_path(self, file_path: str) -> list[dict[str, Any]]:
        """Returns the result of parsing a file path. series and episodes will be
        returned only if the parsing matches to a specific series and one or more
        episodes. series and episodes will be formatted the same as Series and Episode
        responses.

        Args:
            file_path (str): file path of series / episode

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("parse", self.ver_uri, list, {"path": file_path})

    ## RELEASE

    # GET /release
    def get_releases(self, id_: int) -> list[dict[str, Any]]:
        """Get a release with a specific episode ID.

        Args:
            id_ (int): Database id for episode

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("release", self.ver_uri, list, {"episodeId": id_})

    # POST /release
    # TODO: find response
    def download_release(self, guid: str, indexer_id: int) -> Any:
        """Adds a previously searched release to the download client, if the release is
         still in Sonarr's search cache (30 minute cache). If the release is not found
         in the cache Sonarr will return a 404.

        Args:
            guid (str): Recently searched result guid
            indexer_id (int): Database id of indexer to use

        Returns:
            [type]: [description]
        """
        data = {"guid": guid, "indexerId": indexer_id}
        return self._post("release", self.ver_uri, data=data)

    # POST /release/push
    # TODO: find response
    def push_release(
        self, title: str, download_url: str, protocol: str, publish_date: datetime
    ) -> Any:
        """If the title is wanted, Sonarr will grab it.

        Args:
            title (str): Release name
            download_url (str): .torrent file URL
            protocol (str): "Usenet" or "Torrent
            publish_date (datetime): ISO8601 date

        Returns:
            JSON: Array
        """
        data = {
            "title": title,
            "downloadUrl": download_url,
            "protocol": protocol,
            "publishDate": publish_date.isoformat(),
        }
        return self._post("release/push", self.ver_uri, data=data)

    ## SERIES
    # GET /series and /series/{id}
    def get_series(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Returns all series in your collection or the series with the matching
        series ID if one is found.

        Args:
            id_ (Optional[int], optional): Database id for series. Defaults to None.

        Returns:
            list[dict]: List of dictionaries with items
        """
        path = f"series/{id_}" if id_ else "series"
        return self.assert_return(path, self.ver_uri, list)

    # POST /series
    def add_series(
        self,
        tvdb_id: int,
        quality_profile_id: int,
        root_dir: str,
        season_folder: bool = True,
        monitored: bool = True,
        ignore_episodes_with_files: bool = False,
        ignore_episodes_without_files: bool = False,
        search_for_missing_episodes: bool = False,
    ) -> dict[str, Any]:
        """Adds a new series to your collection

        Note:
            if you do not add the required params, then the series wont function. some of these without the others can
            indeed make a "series". But it wont function properly in nzbdrone.

        Args:
            tvdb_id (int): TVDB Id
            quality_profile_id (int): Database id for quality profile
            root_dir (str): Root folder location, full path will be created from this
            season_folder (bool, optional): Create a folder for each season. Defaults to True.
            monitored (bool, optional): Monitor this series. Defaults to True.
            ignore_episodes_with_files (bool, optional): Ignore any episodes with existing files. Defaults to False.
            ignore_episodes_without_files (bool, optional): Ignore any episodes without existing files. Defaults to False.
            search_for_missing_episodes (bool, optional): Search for missing episodes to download. Defaults to False.

        Returns:
            dict[str, Any]: Dictionary of added record
        """
        series_json = self._series_json(
            tvdb_id,
            quality_profile_id,
            root_dir,
            season_folder,
            monitored,
            ignore_episodes_with_files,
            ignore_episodes_without_files,
            search_for_missing_episodes,
        )

        return self._post("series", self.ver_uri, data=series_json)

    # PUT /series
    def upd_series(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing series

        Args:
            data (dict[str, Any]): contains data obtained by get_series()

        Returns:
            dict[str, Any]: Dictionary or updated record
        """
        return self._put("series", self.ver_uri, data=data)

    # DELETE /series/{id}
    def del_series(self, id_: int, delete_files: bool = False) -> Response:
        """Delete the series with the given ID

        Args:
            id_ (int): Database ID for series
            delete_files (bool, optional): If true series folder and files will be deleted. Defaults to False.

        Returns:
            Response: HTTP Response
        """
        # File deletion does not work
        params = {"deleteFiles": delete_files}
        return self._delete(f"series/{id_}", self.ver_uri, params=params)

    # GET /series/lookup
    def lookup_series(self, term: str) -> list[dict[str, Any]]:
        """Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

        Args:
            term (str): Series' Name, using `%20` to signify spaces, as in `The%20Blacklist`

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("series/lookup", self.ver_uri, list, {"term": term})

    # GET /series/lookup
    def lookup_series_by_tvdb_id(self, id_: int) -> list[dict[str, Any]]:
        """Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

        Args:
            id_ (int): TVDB ID

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {"term": f"tvdb:{id_}"}
        return self.assert_return("series/lookup", self.ver_uri, list, params)
