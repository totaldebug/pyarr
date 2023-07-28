from datetime import datetime
from typing import Any, Optional, Union
from warnings import warn

from requests import Response

from pyarr.const import DEPRECATION_WARNING
from pyarr.exceptions import PyarrMissingArgument
from pyarr.types import JsonArray, JsonObject

from .base import BaseArrAPI
from .lib.alias_decorator import alias, aliased
from .models.common import PyarrHistorySortKey, PyarrSortDirection
from .models.sonarr import SonarrCommands, SonarrSortKey


@aliased
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

    # POST /rootfolder
    def add_root_folder(
        self,
        directory: str,
    ) -> JsonObject:
        """Adds a new root folder

        Args:
            directory (str): The directory path

        Returns:
            JsonObject: Dictionary containing path details
        """
        return self._post("rootfolder", self.ver_uri, data={"path": directory})

    ## COMMAND

    # POST /command
    # TODO: Add more logic to ensure correct kwargs for a command
    def post_command(
        self, name: SonarrCommands, **kwargs: Optional[dict[str, Union[int, list[int]]]]
    ) -> JsonObject:
        """Performs any of the predetermined Sonarr command routines

        Args:
            name (SonarrCommands): Command that should be executed
            **kwargs: Additional parameters for specific commands.

        Note:
            For available commands and required `**kwargs` see the `SonarrCommands` model

        Returns:
            JsonObject: Dictionary containing job
        """
        data: dict[str, Any] = {
            "name": name,
        }
        if kwargs:
            data |= kwargs
        return self._post("command", self.ver_uri, data=data)

    ## EPISODE

    # GET /episode
    def get_episode(self, id_: int, series: bool = False) -> JsonObject:
        """Get episodes by ID or series

        Args:
            id_ (int): ID for Episode or Series.
            series (bool, optional): Set to true if the ID is for a Series. Defaults to false.

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get(
            f"episode{'' if series else f'/{id_}'}",
            self.ver_uri,
            params={"seriesId": id_} if series else None,
        )

    # GET /episode
    def get_episodes_by_series_id(self, id_: int) -> JsonArray:
        # sourcery skip: class-extract-method
        """Gets all episodes from a given series ID

        Args:
            id_ (int): Database id for series

        Note:
            This method is deprecated and will be removed in a
            future release. Please use get_episode()

        Returns:
            JsonArray: List of dictionaries with items
        """
        warn(
            f"{DEPRECATION_WARNING} Please use get_episode()",
            DeprecationWarning,
            stacklevel=2,
        )
        params = {"seriesId": id_}
        return self._get("episode", self.ver_uri, params)

    # GET /episode/{id}
    def get_episode_by_episode_id(self, id_: int) -> JsonObject:
        """Gets a specific episode by database id

        Args:
            id_ (int): Database id for episode

        Note:
            This method is deprecated and will be removed in a
            future release. Please use get_episode()

        Returns:
            JsonArray: List of dictionaries with items
        """
        warn(
            f"{DEPRECATION_WARNING} Please use get_episode()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._get(f"episode/{id_}", self.ver_uri)

    # PUT /episode
    def upd_episode(self, id_: int, data: JsonObject) -> JsonObject:
        """Update the given episodes, currently only monitored is supported

        Args:
            id_ (int): ID of the Episode to be updated
            data (dict[str, Any]): Parameters to update the episode

        Example:
            ::

                payload = {"monitored": True}
                sonarr.upd_episode(1, payload)

        Returns:
            JsonObject: Dictionary with updated record
        """
        return self._put(f"episode/{id_}", self.ver_uri, data=data)

    # PUT /episode/monitor
    def upd_episode_monitor(
        self, episode_ids: list[int], monitored: bool = True
    ) -> JsonArray:
        """Update episode monitored status

        Args:
            episode_ids (list[int]): All episode IDs to be updated
            monitored (bool, optional): True or False. Defaults to True.

        Returns:
            JsonArray: list of dictionaries containing updated records
        """
        return self._put(
            "episode/monitor",
            self.ver_uri,
            data={"episodeIds": episode_ids, "monitored": monitored},
        )

    ## EPISODE FILE

    # GET /episodefile
    def get_episode_files_by_series_id(self, id_: int) -> JsonArray:
        """Returns all episode file information for series id specified

        Args:
            id_ (int): Database id of series

        Returns:
            JsonArray: List of dictionaries with items
        """
        warn(
            f"{DEPRECATION_WARNING} Please use get_episode_file()",
            DeprecationWarning,
            stacklevel=2,
        )
        params = {"seriesId": id_}
        return self._get("episodefile", self.ver_uri, params)

    # GET /episodefile/{id}
    def get_episode_file(self, id_: int, series: bool = False) -> JsonObject:
        """Returns episode file information for specified id

        Args:
            id_ (int): Database id of episode file
            series (bool, optional): Set to true if the ID is for a Series. Defaults to false.

        Returns:
            JsonObject: Dictionary with data
        """
        return self._get(
            f"episodefile{'' if series else f'/{id_}'}",
            self.ver_uri,
            params={"seriesId": id_} if series else None,
        )

    # DELETE /episodefile/{id}
    def del_episode_file(self, id_: int) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Deletes the episode file with corresponding id

        Args:
            id_ (int): Database id for episode file

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"episodefile/{id_}", self.ver_uri)

    # PUT /episodefile/{id}
    def upd_episode_file_quality(self, id_: int, data: JsonObject) -> JsonObject:
        """Updates the quality of the episode file and returns the episode file

        Args:
            id_ (int): Database id for episode file
            data (JsonObject): data with quality::

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
            JsonObject: Dictionary with updated record
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
    ) -> JsonObject:
        """Gets missing episode (episodes without files)

        Args:
            page (Optional[int], optional): Page number to return. Defaults to None.
            page_size (Optional[int], optional): Number of items per page. Defaults to None.
            sort_key (Optional[SonarrSortKey], optional): series.title or airDateUtc. Defaults to None.
            sort_dir (Optional[PyarrSortDirection], optional): Direction to sort the items. Defaults to None.
            include_series (Optional[bool], optional): Include the whole series. Defaults to None

        Returns:
            JsonObject: Dictionary with items
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
    ) -> JsonObject:
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
            JsonObject: Dictionary with queue items
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
    ) -> JsonObject:
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
            JsonObject: Dictionary with items
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
    def get_parsed_title(self, title: str) -> JsonObject:
        """Returns the result of parsing a title. series and episodes will be
        returned only if the parsing matches to a specific series and one or more
        episodes. series and episodes will be formatted the same as Series and Episode
        responses.

        Args:
            title (str): Title of series / episode

        Returns:
            JsonObject: List of dictionaries with items
        """
        warn(
            f"{DEPRECATION_WARNING} Please use get_parse_title_path()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._get("parse", self.ver_uri, {"title": title})

    # GET /parse
    def get_parsed_path(self, file_path: str) -> JsonObject:
        """Returns the result of parsing a file path. series and episodes will be
        returned only if the parsing matches to a specific series and one or more
        episodes. series and episodes will be formatted the same as Series and Episode
        responses.

        Args:
            file_path (str): file path of series / episode

        Returns:
            JsonObject: List of dictionaries with items
        """
        warn(
            f"{DEPRECATION_WARNING} Please use get_parse_title_path()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._get("parse", self.ver_uri, {"path": file_path})

    ## RELEASE

    # GET /release
    @alias("get_releases", deprecated_version="6.0.0")
    def get_release(self, id_: Optional[int] = None) -> JsonArray:
        """Query indexers for latest releases.

        Args:
            id_ (int): Database id for episode to check

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("release", self.ver_uri, {"episodeId": id_} if id_ else None)

    # POST /release
    @alias("download_release", "6.0.0")
    def post_release(self, guid: str, indexer_id: int) -> JsonObject:
        """Adds a previously searched release to the download client, if the release is
         still in Sonarr's search cache (30 minute cache). If the release is not found
         in the cache Sonarr will return a 404.

        Args:
            guid (str): Recently searched result guid
            indexer_id (int): Database id of indexer to use

        Returns:
            JsonObject: Dictionary with download release details
        """
        data = {"guid": guid, "indexerId": indexer_id}
        return self._post("release", self.ver_uri, data=data)

    # POST /release/push
    # TODO: find response
    @alias("push_release", "6.0.0")
    def post_release_push(
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
        self, id_: Optional[int] = None, tvdb: Optional[bool] = False
    ) -> Union[JsonArray, JsonObject]:
        """Returns all series in your collection or the series with the matching
        series ID if one is found.

        Args:
            id_ (Optional[int], optional): Database id for series. Defaults to None.
            tvdb (Optional[bool], optional): Set to true if ID is tvdb. Defaults to False

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items, or a
            dictionary with single item
        """
        if id_ and tvdb:
            path = f"series?tvdbId={id_}"
        else:
            path = f"series{f'/{id_}' if id_ else ''}"
        return self._get(path, self.ver_uri)

    # POST /series
    def add_series(
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
        """Adds a new series to your collection

        Note:
            if you do not add the required params, then the series wont function. some of these without the others can
            indeed make a "series". But it wont function properly in nzbdrone.

        Args:
            series (JsonObject): A series object from `lookup()`
            quality_profile_id (int): Database id for quality profile
            language_profile_id (int): Database id for language profile
            root_dir (str): Root folder location, full path will be created from this
            season_folder (bool, optional): Create a folder for each season. Defaults to True.
            monitored (bool, optional): Monitor this series. Defaults to True.
            ignore_episodes_with_files (bool, optional): Ignore any episodes with existing files. Defaults to False.
            ignore_episodes_without_files (bool, optional): Ignore any episodes without existing files. Defaults to False.
            search_for_missing_episodes (bool, optional): Search for missing episodes to download. Defaults to False.

        Returns:
            JsonObject: Dictionary of added record
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

        return self._post("series", self.ver_uri, data=series)

    # PUT /series
    def upd_series(self, data: JsonObject) -> JsonObject:
        """Update an existing series

        Args:
            data (JsonObject): contains data obtained by get_series()

        Returns:
            JsonObject: Dictionary or updated record
        """
        return self._put("series", self.ver_uri, data=data)

    # DELETE /series/{id}
    def del_series(
        self, id_: int, delete_files: bool = False
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
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
    ) -> JsonArray:
        """Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

        Args:
            term (Optional[str], optional): Series' Name
            id_ (Optional[int], optional): TVDB ID for series

        Returns:
            JsonArray: List of dictionaries with items
        """
        if term is None and id_ is None:
            raise PyarrMissingArgument("A term or TVDB id must be included")

        return self._get("series/lookup", self.ver_uri, {"term": term or f"tvdb:{id_}"})

    # GET /series/lookup
    def lookup_series_by_tvdb_id(self, id_: int) -> JsonArray:
        """Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

        Note:
            This method is deprecated and will be removed in a future release. Please use lookup_series()

        Args:
            id_ (int): TVDB ID

        Returns:
            JsonArray: List of dictionaries with items
        """
        warn(
            f"{DEPRECATION_WARNING} Please use lookup_series()",
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
    ) -> JsonObject:
        """Gets history (grabs/failures/completed)

        Args:
            page (Optional[int], optional): Page number to return. Defaults to None.
            page_size (Optional[int], optional): Number of items per page. Defaults to None.
            sort_key (Optional[PyarrHistorySortKey], optional): Field to sort by. Defaults to None.
            sort_dir (Optional[PyarrSortDirection], optional): Direction to sort the items. Defaults to None.
            id_ (Optional[int], optional): Filter to a specific episode ID. Defaults to None.

        Returns:
           JsonObject: Dictionary with items
        """
        params: dict[
            str,
            Union[int, PyarrHistorySortKey, PyarrSortDirection],
        ] = {}

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

    # GET /languageprofile/{id}
    def get_language_profile(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, dict[Any, Any]]:
        """Gets all language profiles or specific one with id

        Args:
            id_ (Optional[int], optional): Language profile id from database. Defaults to None.

        Note:
            This method is deprecated and will be removed in a
            future release. Please use get_language()

        Returns:
            Union[JsonArray, dict[Any, Any]]: List of dictionaries with items
        """
        warn(
            f"{DEPRECATION_WARNING} Please use get_language()",
            DeprecationWarning,
            stacklevel=2,
        )

        path = f"languageprofile{f'/{id_}' if id_ else ''}"
        return self._get(path, self.ver_uri)

    # GET /languageprofile/schema/{id}
    def get_language_profile_schema(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, dict[Any, Any]]:
        """Gets all language profile schemas or specific one with id

        Args:
            id_ (Optional[int], optional): Language profile schema id from database. Defaults to None.

        Returns:
            Union[JsonArray, dict[Any, Any]]: List of dictionaries with items
        """

        path = f"languageprofile/schema{f'/{id_}' if id_ else ''}"
        return self._get(path, self.ver_uri)

    # POST /qualityprofile
    def add_quality_profile(
        self, name: str, upgrades_allowed: bool, cutoff: int, items: list
    ) -> JsonObject:
        """Add new quality profile

        Args:
            name (str): Name of the profile
            upgrades_allowed (bool): Are upgrades in quality allowed?
            cutoff (int): ID of quality definition to cutoff at. Must be an allowed definition ID.
            items (list): Add a list of items (from `get_quality_definition()`)

        Returns:
            JsonObject: An object containing the profile
        """
        data = {
            "name": name,
            "upgradeAllowed": upgrades_allowed,
            "cutoff": cutoff,
            "items": items,
        }
        return self._post("qualityprofile", self.ver_uri, data=data)

    # GET /manualimport
    def get_manual_import(
        self,
        folder: str,
        download_id: Optional[str] = None,
        series_id: Optional[int] = None,
        filter_existing_files: Optional[bool] = None,
        replace_existing_files: Optional[bool] = None,
    ) -> JsonArray:
        """Gets a manual import list

        Args:
            downloadId (str): Download IDs
            series_id (int, optional): Series Database ID. Defaults to None.
            folder (Optional[str], optional): folder name. Defaults to None.
            filterExistingFiles (bool, optional): filter files. Defaults to True.
            replaceExistingFiles (bool, optional): replace files. Defaults to True.

        Returns:
            JsonArray: List of dictionaries with items
        """
        params: dict[str, Union[str, int, bool]] = {"folder": folder}
        if download_id:
            params["downloadId"] = download_id
        if series_id:
            params["seriesId"] = series_id
        if filter_existing_files:
            params["filterExistingFiles"] = filter_existing_files
        if replace_existing_files:
            params["replaceExistingFiles"] = replace_existing_files

        return self._get("manualimport", self.ver_uri, params=params)

    # PUT /manualimport
    def upd_manual_import(self, data: JsonObject) -> JsonObject:
        """Update a manual import

        Note:
            To be used in conjunction with get_manual_import()

        Args:
            data (JsonObject): Data containing changes

        Returns:
            JsonObject: Dictionary of updated record
        """
        return self._put("manualimport", self.ver_uri, data=data)
