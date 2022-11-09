from datetime import datetime
from typing import Any, Optional, Union
from warnings import warn

from requests import Response

from pyarr.exceptions import PyarrMissingArgument
from pyarr.types import JsonDataType

from .base import BaseArrAPI
from .models.common import PyarrHistorySortKey, PyarrSortDirection
from .models.sonarr import SonarrCommands, SonarrSortKey


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
        series: dict[str, Any] = self.lookup_series_by_tvdb_id(tvdb_id)[0]
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

    # POST /rootfolder
    def add_root_folder(
        self,
        directory: str,
    ) -> dict[str, JsonDataType]:
        """Adds a new root folder

        Args:
            directory (str): The directory path

        Returns:
            dict[str, JsonDataType]: Dictionary containing path details
        """
        return self._post("rootfolder", self.ver_uri, data={"path": directory})

    ## COMMAND

    # GET /command
    def get_command(
        self, id_: Optional[int] = None
    ) -> Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]:
        """Queries the status of a previously started command, or all currently started commands.

        Args:
            id_ (Optional[int], optional): Database ID of the command. Defaults to None.

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        path = f"command{f'/{id_}' if id_ else ''}"
        return self._get(path, self.ver_uri)

    # POST /command
    # TODO: Add more logic to ensure correct kwargs for a command
    # TODO: look into DownloadedEpisodesScan and how to use it
    def post_command(
        self, name: SonarrCommands, **kwargs: Optional[Union[int, list[int]]]
    ) -> dict[str, JsonDataType]:
        """Performs any of the predetermined Sonarr command routines

        Args:
            name (SonarrCommands): Command that should be executed
            **kwargs: Additional parameters for specific commands. See note.

        Note:
            Required Kwargs:
                RefreshSeries: seriesId (int, optional) - If not set, all series will be refreshed and scanned
                RescanSeries: seriesId (int, optional) - If not set all series will be scanned
                EpisodeSearch: episodeIds (lsit[int], optional) - One or more episodeIds in a list
                SeasonSearch: seriesId (int) seasonNumber (int)
                SeriesSearch: seriesId (int)
                DownloadedEpisodesScan:
                RssSync: None
                RenameFiles: files (list[int]) - List of File IDs to rename
                RenameSeries: seriesIds (list[int]) List of Series IDs to rename
                Backup: None
                missingEpisodeSearch: None

        Returns:
            dict[str, JsonDataType]: Dictionary containing job
        """
        data: dict[str, Any] = {
            "name": name,
        }
        if kwargs:
            data |= kwargs
        return self._post("command", self.ver_uri, data=data)

    ## EPISODE

    # GET /episode
    def get_episode(self, id_: int, series: bool = False) -> dict[str, JsonDataType]:
        """Get get episodes by ID or series

        Args:
            id_ (int): ID for Episode or Series.
            series (bool, optional): Set to true if the ID is for a Series. Defaults to false.

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        return self._get(
            f"episode{'' if series else f'/{id_}'}",
            self.ver_uri,
            params={"seriesId": id_} if series else None,
        )

    # GET /episode
    def get_episodes_by_series_id(self, id_: int) -> list[dict[str, JsonDataType]]:
        # sourcery skip: class-extract-method
        """Gets all episodes from a given series ID

        Args:
            id_ (int): Database id for series

        Note:
            This method is deprecated and will be removed in a
            future release. Please use get_episode()

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. Please use get_episode()",
            DeprecationWarning,
            stacklevel=2,
        )
        params = {"seriesId": id_}
        return self._get("episode", self.ver_uri, params)

    # GET /episode/{id}
    def get_episode_by_episode_id(self, id_: int) -> dict[str, JsonDataType]:
        """Gets a specific episode by database id

        Args:
            id_ (int): Database id for episode

        Note:
            This method is deprecated and will be removed in a
            future release. Please use get_episode()

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. Please use get_episode()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._get(f"episode/{id_}", self.ver_uri)

    # PUT /episode
    def upd_episode(
        self, id_: int, data: dict[str, JsonDataType]
    ) -> dict[str, JsonDataType]:
        """Update the given episodes, currently only monitored is supported

        Args:
            id_ (int): ID of the Episode to be updated
            data (dict[str, Any]): Parameters to update the episode

        Example:
            ::

                payload = {"monitored": True}
                sonarr.upd_episode(1, payload)

        Returns:
            dict[str, JsonDataType]: Dictionary with updated record
        """
        return self._put(f"episode/{id_}", self.ver_uri, data=data)

    ## EPISODE FILE

    # GET /episodefile
    def get_episode_files_by_series_id(self, id_: int) -> list[dict[str, JsonDataType]]:
        """Returns all episode file information for series id specified

        Args:
            id_ (int): Database id of series

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. Please use get_episode_file()",
            DeprecationWarning,
            stacklevel=2,
        )
        params = {"seriesId": id_}
        return self._get("episodefile", self.ver_uri, params)

    # GET /episodefile/{id}
    def get_episode_file(
        self, id_: int, series: bool = False
    ) -> dict[str, JsonDataType]:
        """Returns episode file information for specified id

        Args:
            id_ (int): Database id of episode file
            series (bool, optional): Set to true if the ID is for a Series. Defaults to false.

        Returns:
            dict[str, JsonDataType]: Dictionary with data
        """
        return self._get(
            f"episodefile{'' if series else f'/{id_}'}",
            self.ver_uri,
            params={"seriesId": id_} if series else None,
        )

    # DELETE /episodefile/{id}
    def del_episode_file(
        self, id_: int
    ) -> Union[Response, dict[str, JsonDataType], dict[Any, Any]]:
        """Deletes the episode file with corresponding id

        Args:
            id_ (int): Database id for episode file

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"episodefile/{id_}", self.ver_uri)

    # PUT /episodefile/{id}
    def upd_episode_file_quality(
        self, id_: int, data: dict[str, JsonDataType]
    ) -> dict[str, JsonDataType]:
        """Updates the quality of the episode file and returns the episode file

        Args:
            id_ (int): Database id for episode file
            data (dict[str, JsonDataType]): data with quality::

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
            dict[str, JsonDataType]: Dictionary with updated record
        """
        return self._put(f"episodefile/{id_}", self.ver_uri, data=data)

    # GET /wanted/missing
    def get_wanted(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_key: Optional[SonarrSortKey] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
        include_series: Optional[bool] = None,
    ) -> dict[str, JsonDataType]:
        """Gets missing episode (episodes without files)

        Args:
            page (Optional[int], optional): Page number to return. Defaults to None.
            page_size (Optional[int], optional): Number of items per page. Defaults to None.
            sort_key (Optional[SonarrSortKey], optional): series.title or airDateUtc. Defaults to None.
            sort_dir (Optional[PyarrSortDirection], optional): Direction to sort the items. Defaults to None.
            include_series (Optional[bool], optional): Include the whole series. Defaults to None

        Returns:
            dict[str, JsonDataType]: Dictionary with items
        """
        params: dict[str, Union[int, SonarrSortKey, PyarrSortDirection, bool]] = {}
        if page:
            params["page"] = page
        if page_size:
            params["pageSize"] = page_size
        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir  must be used together")
        if include_series:
            params["includeSeries"] = include_series

        return self._get("wanted/missing", self.ver_uri, params)

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_key: Optional[SonarrSortKey] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
        include_unknown_series_items: Optional[bool] = None,
        include_series: Optional[bool] = None,
        include_episode: Optional[bool] = None,
    ) -> dict[str, JsonDataType]:
        """Gets currently downloading info

        Args:
            page (Optional[int], optional): Page number to return. Defaults to None.
            page_size (Optional[int], optional): Number of items per page. Defaults to None.
            sort_key (Optional[SonarrSortKey], optional): Field to sort by. Defaults to None.
            sort_dir (Optional[PyarrSortDirection], optional): Direction to sort the items. Defaults to None.
            include_unknown_series_items (Optional[bool], optional): Include unknown series items. Defaults to None.
            include_series (Optional[bool], optional): Include series. Defaults to None.
            include_episode (Optional[bool], optional): Include episodes. Defaults to None.

        Returns:
            dict[str, JsonDataType]: Dictionary with queue items
        """
        params: dict[str, Union[int, bool, SonarrSortKey, PyarrSortDirection]] = {}

        if page:
            params["page"] = page
        if page_size:
            params["pageSize"] = page_size
        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir  must be used together")
        if include_unknown_series_items is not None:
            params["includeUnknownSeriesItems"] = include_unknown_series_items
        if include_series is not None:
            params["includeSeries"] = include_series
        if include_episode is not None:
            params["includeEpisode"] = include_episode

        return self._get("queue", self.ver_uri, params)

    ## PARSE

    def get_parse_title_path(
        self, title: Optional[str] = None, path: Optional[str] = None
    ) -> dict[str, JsonDataType]:
        """Returns the result of parsing a title or path. series and episodes will be
        returned only if the parsing matches to a specific series and one or more
        episodes. series and episodes will be formatted the same as Series and Episode
        responses.

        Args:
            title (Optional[str], optional): Title of series or episode. Defaults to None.
            path (Optional[str], optional): file path of series or episode. Defaults to None.

        Raises:
            PyarrMissingArgument: If no argument is passed, error

        Returns:
            dict[str, JsonDataType]: Dictionary with items
        """
        if title is None and path is None:
            raise PyarrMissingArgument("A title or path must be specified")
        params = {}
        if title is not None:
            params["title"] = title
        if path is not None:
            params["path"] = path
        return self._get("parse", self.ver_uri, params)

    # GET /parse
    def get_parsed_title(self, title: str) -> dict[str, JsonDataType]:
        """Returns the result of parsing a title. series and episodes will be
        returned only if the parsing matches to a specific series and one or more
        episodes. series and episodes will be formatted the same as Series and Episode
        responses.

        Args:
            title (str): Title of series / episode

        Returns:
            dict[str, JsonDataType]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. Please use get_parse_title_path()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._get("parse", self.ver_uri, {"title": title})

    # GET /parse
    def get_parsed_path(self, file_path: str) -> dict[str, JsonDataType]:
        """Returns the result of parsing a file path. series and episodes will be
        returned only if the parsing matches to a specific series and one or more
        episodes. series and episodes will be formatted the same as Series and Episode
        responses.

        Args:
            file_path (str): file path of series / episode

        Returns:
            dict[str, JsonDataType]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. Please use get_parse_title_path()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._get("parse", self.ver_uri, {"path": file_path})

    ## RELEASE

    # GET /release
    def get_releases(self, id_: Optional[int] = None) -> list[dict[str, JsonDataType]]:
        """Query indexers for latest releases.

        Args:
            id_ (int): Database id for episode to check

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        return self._get("release", self.ver_uri, {"episodeId": id_} if id_ else None)

    # POST /release
    def download_release(self, guid: str, indexer_id: int) -> dict[str, JsonDataType]:
        """Adds a previously searched release to the download client, if the release is
         still in Sonarr's search cache (30 minute cache). If the release is not found
         in the cache Sonarr will return a 404.

        Args:
            guid (str): Recently searched result guid
            indexer_id (int): Database id of indexer to use

        Returns:
            dict[str, JsonDataType]: Dictionary with download release details
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
    def get_series(
        self, id_: Optional[int] = None
    ) -> Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]:
        """Returns all series in your collection or the series with the matching
        series ID if one is found.

        Args:
            id_ (Optional[int], optional): Database id for series. Defaults to None.

        Returns:
            Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]: List of dictionaries with items, or a
            dictionary with single item
        """
        path = f"series{f'/{id_}' if id_ else ''}"
        return self._get(path, self.ver_uri)

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
    ) -> dict[str, JsonDataType]:
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
            dict[str, JsonDataType]: Dictionary of added record
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
    def upd_series(self, data: dict[str, JsonDataType]) -> dict[str, JsonDataType]:
        """Update an existing series

        Args:
            data (dict[str, JsonDataType]): contains data obtained by get_series()

        Returns:
            dict[str, JsonDataType]: Dictionary or updated record
        """
        return self._put("series", self.ver_uri, data=data)

    # DELETE /series/{id}
    def del_series(
        self, id_: int, delete_files: bool = False
    ) -> Union[Response, dict[str, JsonDataType], dict[Any, Any]]:
        """Delete the series with the given ID

        Args:
            id_ (int): Database ID for series
            delete_files (bool, optional): If true series folder and files will be deleted. Defaults to False.

        Returns:
            dict: Blank dictionary
        """
        # File deletion does not work
        params = {"deleteFiles": delete_files}
        return self._delete(f"series/{id_}", self.ver_uri, params=params)

    # GET /series/lookup
    def lookup_series(
        self, term: Optional[str] = None, id_: Optional[int] = None
    ) -> list[dict[str, JsonDataType]]:
        """Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

        Args:
            term (Optional[str], optional): Series' Name
            id_ (Optional[int], optional): TVDB ID for series

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        if term is None and id_ is None:
            raise PyarrMissingArgument("A term or TVDB id must be included")

        return self._get("series/lookup", self.ver_uri, {"term": term or f"tvdb:{id_}"})

    # GET /series/lookup
    def lookup_series_by_tvdb_id(self, id_: int) -> list[dict[str, JsonDataType]]:
        """Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

        Args:
            id_ (int): TVDB ID

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. Please use lookup_series()",
            DeprecationWarning,
            stacklevel=2,
        )
        params = {"term": f"tvdb:{id_}"}
        return self._get("series/lookup", self.ver_uri, params)

    # GET /history
    # Overrides base get history for ID
    def get_history(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_key: Optional[PyarrHistorySortKey] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
        id_: Optional[int] = None,
    ) -> dict[str, JsonDataType]:
        """Gets history (grabs/failures/completed)

        Args:
            page (Optional[int], optional): Page number to return. Defaults to None.
            page_size (Optional[int], optional): Number of items per page. Defaults to None.
            sort_key (Optional[PyarrHistorySortKey], optional): Field to sort by. Defaults to None.
            sort_dir (Optional[PyarrSortDirection], optional): Direction to sort the items. Defaults to None.
            id_ (Optional[int], optional): Filter to a specific episode ID. Defaults to None.

        Returns:
           dict[str, JsonDataType]: Dictionary with items
        """
        params: dict[str, Union[int, PyarrHistorySortKey, PyarrSortDirection]] = {}

        if page:
            params["page"] = page

        if page_size:
            params["pageSize"] = page_size

        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir  must be used together")

        if id_:
            params["episodeId"] = id_

        return self._get("history", self.ver_uri, params)
