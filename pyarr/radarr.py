from datetime import datetime
from typing import Any, Optional, Union
from warnings import warn

from requests import Response

from pyarr.const import DEPRECATION_WARNING
from pyarr.types import JsonArray, JsonObject

from .base import BaseArrAPI
from .exceptions import PyarrMissingArgument
from .models.common import PyarrSortDirection
from .models.radarr import (
    RadarrAvailabilityType,
    RadarrCommands,
    RadarrEventType,
    RadarrMonitorType,
    RadarrSortKey,
)


class RadarrAPI(BaseArrAPI):
    """API wrapper for Radarr endpoints.

    Args:
        RequestAPI (:obj:`str`): provides connection to API endpoint
    """

    def __init__(self, host_url: str, api_key: str):
        """Initialize the Radarr API.

        Args:
            host_url (str): URL for Radarr
            api_key (str): API key for Radarr
        """

        ver_uri = "/v3"
        super().__init__(host_url, api_key, ver_uri)

    ## CONFIG
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

    ## MOVIE

    # GET /movie
    def get_movie(
        self, id_: Optional[int] = None, tmdb: bool = False
    ) -> Union[JsonArray, JsonObject]:  # sourcery skip: class-extract-method
        """Returns all movies in the database, movie based on the Radarr ID or TMDB id.

        Note:
            IMDB is not supported at this time

        Args:
            id_ (Optional[int], optional): Radarr ID or TMDB ID of Movies. Defaults to None.
            tmdb (bool): Use TMDB Id. Defaults to False

        Returns:
            Union[JsonArray, JsonObject]: List or Dictionary with items
        """
        params = {}
        if tmdb:
            params["tmdbid"] = id_

        return self._get(
            f"movie{'' if id_ is None or tmdb else f'/{id_}'}",
            self.ver_uri,
            params=params,
        )

    # POST /movie
    def add_movie(
        self,
        movie: JsonObject,
        root_dir: str,
        quality_profile_id: int,
        monitored: bool = True,
        search_for_movie: bool = True,
        monitor: RadarrMonitorType = "movieOnly",
        minimum_availability: RadarrAvailabilityType = "announced",
        tags: list[int] = [],
    ) -> JsonObject:
        """Adds a movie to the database

        Args:
            movie (JsonObject): Movie record from `lookup_movie()`
            root_dir (str): Location of the root DIR
            quality_profile_id (int): ID of the quality profile the movie will use
            monitored (bool, optional): Should the movie be monitored. Defaults to True.
            search_for_movie (bool, optional): Should we search for the movie. Defaults to True.
            monitor (RadarrMonitorType, optional): Monitor movie or collection. Defaults to "movieOnly".
            minimum_availability (RadarrAvailabilityType, optional): Availability of movie. Defaults to "announced"
            tags (list[int], optional): List of tag id's. Defaults to [].

        Returns:
            JsonObject: Dictonary with added record
        """
        movie["rootFolderPath"] = root_dir
        movie["qualityProfileId"] = quality_profile_id
        movie["monitored"] = monitored
        movie["minimumAvailability"] = minimum_availability
        movie["addOptions"] = {
            "monitor": monitor,
            "searchForMovie": search_for_movie,
        }
        movie["tags"] = tags

        return self._post("movie", self.ver_uri, data=movie)

    # PUT /movie
    def upd_movie(
        self,
        data: JsonObject,
        move_files: Optional[bool] = None,
    ) -> JsonObject:
        """Updates a movie in the database.

        Args:
            data (JsonObject): Dictionary containing an object obtained from get_movie()
            move_files (Optional[bool], optional): Have radarr move files when updating. Defaults to None.

        Returns:
            JsonObject: Dictionary with updated record
        """
        params = {}
        if move_files is not None:
            params["moveFiles"] = move_files
        print(type(data))
        return self._put(
            "movie",
            self.ver_uri,
            data=data,
            params=params,
        )

    # GET /movie/{id}
    def get_movie_by_movie_id(self, id_: int) -> JsonObject:
        """Get a movie by the Radarr database ID

        Args:
            id_ (int): Database Id of movie to return

        Note:
            This method is deprecated and will be removed in a
            future release. Please use get_movie()

        Returns:
            JsonArray: List of dictionaries with items
        """
        warn(
            f"{DEPRECATION_WARNING} Please use get_movie()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._get(f"movie/{id_}", self.ver_uri)

    # DELETE /movie/{id}
    def del_movie(
        self,
        id_: Union[int, list],
        delete_files: Optional[bool] = None,
        add_exclusion: Optional[bool] = None,
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete a single movie or multiple movies by database id.

        Args:
            id_ (Union[int, list]): Int with single movie Id or list with multiple IDs to delete.
            delete_files (bool, optional): Delete movie files when deleting movies. Defaults to None.
            add_exclusion (bool, optional): Add deleted movies to List Exclusions. Defaults to None.

        Returns:
            Response: HTTP Response
        """
        params: dict[str, Union[str, list[int], int]] = {}
        if isinstance(id_, list):
            params["movieIds"] = id_
        if delete_files:
            params["deleteFiles"] = delete_files

        if add_exclusion:
            params["addImportExclusion"] = add_exclusion

            print(params)
        return self._delete(
            "movie/editor" if isinstance(id_, list) else f"movie/{id_}",
            self.ver_uri,
            params=None if isinstance(id_, list) else params,
            data=params if isinstance(id_, list) else None,
        )

    # GET /movie/lookup
    def lookup_movie(self, term: str) -> JsonArray:
        """Search for a movie to add to the database (Uses TMDB for search results)

        Args:
            term (str): Search term to use for lookup, can also do IMDB & TMDB IDs::

                radarr.lookup_movie(term="imdb:123456")
                radarr.lookup_movie(term="tmdb:123456")

        Returns:
            JsonArray: List of dictionaries with items
        """
        params = {"term": term}
        return self._get("movie/lookup", self.ver_uri, params)

    # GET /movie/lookup
    def lookup_movie_by_tmdb_id(self, id_: int) -> JsonArray:
        """Search for movie by TMDB ID

        Args:
            id_ (str): TMDB ID

        Returns:
            JsonArray: List of dictionaries with items
        """
        warn(
            f"{DEPRECATION_WARNING} use lookup_movie(term='tmdb:123456')",
            DeprecationWarning,
            stacklevel=2,
        )
        params = {"term": f"tmdb:{id_}"}
        return self._get("movie/lookup", self.ver_uri, params)

    # GET /movie/lookup
    def lookup_movie_by_imdb_id(self, id_: str) -> JsonArray:
        """Search for movie by IMDB ID

        Args:
            id_ (str): IMDB ID

        Returns:
            JsonArray: List of dictionaries with items
        """
        warn(
            f"{DEPRECATION_WARNING} use lookup_movie(term='imdb:123456')",
            DeprecationWarning,
            stacklevel=2,
        )
        params = {"term": f"imdb:{id_}"}
        return self._get("movie/lookup", self.ver_uri, params)

    # PUT /movie/editor
    def upd_movies(self, data: JsonObject) -> JsonArray:
        """The Updates operation allows to edit properties of multiple movies at once

        Args:
            data (JsonObject): Updated movie information::

                {"movieIds":[28],"tags":[3],"applyTags":"add"}
                {"movieIds":[28],"monitored":true}
                {"movieIds":[28],"qualityProfileId":1}
                {"movieIds":[28],"minimumAvailability":"inCinemas"}
                {"movieIds":[28],"rootFolderPath":"/defaults/"}

        Returns:
            JsonArray: Dictionary containing updated record
        """

        return self._put("movie/editor", self.ver_uri, data=data)

    # DELETE /movie/editor
    def del_movies(
        self, data: JsonObject
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """The delete operation allows mass deletion of movies (and optionally files)

        Args:
            data (JsonObject): dictionary of movies to be deleted::

                {
                    "movieIds": [
                        0
                    ],
                    "deleteFIles": true,
                    "addImportExclusion": true
                }

        Returns:
            Response: HTTP Response
        """
        warn(
            f"{DEPRECATION_WARNING} Please use del_movie().",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._delete("movie/editor", self.ver_uri, data=data)

    # POST /movie/import
    def import_movies(self, data: JsonArray) -> JsonArray:
        """The movie import endpoint is used by the bulk import view in Radarr UI. It allows movies to be bulk added to the Radarr database.

        Args:
            data (JsonObject): dictionary of all movies to be imported

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._post("movie/import", self.ver_uri, data=data)

    ## MOVIEFILE

    # GET /moviefile
    # TODO: merge this with get_movie_file
    def get_movie_files_by_movie_id(self, id_: int) -> JsonArray:
        """Get a movie file object by Movie database ID.

        Args:
            id_ (int): Movie database ID

        Returns:
            JsonArray: List of dictionaries with items
        """

        params = {"movieId": id_}
        return self._get("moviefile", self.ver_uri, params)

    # GET /moviefile
    def get_movie_file(self, id_: Union[int, list]) -> JsonArray:
        """Get movie file by database ID

        Args:
            id_ (int, list): Movie file ID, or multiple in a list

        Returns:
            JsonArray: List of dictionaries with items
        """
        if not isinstance(id_, list):
            return self._get(f"moviefile/{id_}", self.ver_uri)
        params = [("movieFileIds", file) for file in id_]
        return self._get("moviefile", self.ver_uri, params=params)

    # DELETE /moviefile/{id}
    def del_movie_file(
        self, id_: Union[int, list]
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Allows for deletion of a moviefile by its database ID.

        Args:
            id_ (Union[int, list]): Movie file ID

        Returns:
            Response: HTTP Response
        """

        if isinstance(id_, list):
            data = {"movieFileIds": id_}
        return self._delete(
            "moviefile/bulk" if isinstance(id_, list) else f"moviefile/{id_}",
            self.ver_uri,
            data=data if isinstance(id_, list) else None,
        )

    # GET /history/movie
    def get_movie_history(
        self, id_: int, event_type: Optional[RadarrEventType] = None
    ) -> JsonArray:
        """Get history for a given movie in database by its database ID

        Args:
            id_ (int): Database ID of movie
            event_type (Optional[RadarrEventType], optional): History event type to retrieve. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items
        """
        params: dict[str, Union[int, str, RadarrEventType]] = {"movieId": id_}
        if event_type:
            params["eventType"] = event_type
        return self._get("history/movie", self.ver_uri, params)

    ## BLOCKLIST

    # GET /blocklist/movie
    def get_blocklist_by_movie_id(
        self,
        id_: int,
    ) -> JsonArray:
        """Retrieves blocklisted releases that are tied to a given movie in the database.

        Args:
            id_ (int): Movie id from Database

        Returns:
            JsonArray: List of dictionaries with items
        """
        params = {"movieId": id_}
        return self._get("blocklist/movie", self.ver_uri, params)

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
        sort_key: Optional[RadarrSortKey] = None,
        include_unknown_movie_items: Optional[bool] = None,
    ) -> JsonObject:
        """Return a list of items in the queue

        Args:
            page (Optional[int], optional): Page to be returned. Defaults to None.
            page_size (Optional[int], optional): Number of results per page. Defaults to None.
            sort_direction (Optional[PyarrSortDirection], optional): Direction to sort. Defaults to None.
            sort_key (Optional[RadarrSortKey], optional): Field to sort. Defaults to None.
            include_unknown_movie_items (Optional[bool], optional): Include unknown movie items. Defaults to None.

        Returns:
            JsonObject: List of dictionaries with items
        """
        params: dict[str, Union[int, PyarrSortDirection, RadarrSortKey, bool]] = {}

        if page:
            params["page"] = page
        if page_size:
            params["pageSize"] = page_size
        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir  must be used together")
        if include_unknown_movie_items is not None:
            params["includeUnknownMovieItems"] = include_unknown_movie_items

        return self._get("queue", self.ver_uri, params)

    # GET /queue/details
    def get_queue_details(
        self,
        id_: Optional[int] = None,
        include_movie: Optional[bool] = None,
    ) -> JsonArray:
        """Get details of all items in queue

        Args:
            id_ (Optional[int], optional): select specific item by id. Defaults to None
            include_movie (Optional[bool], optional): Include movie object if linked. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items
        """
        params = {}
        if id_:
            params["movieId"] = id_
        if include_movie is not None:
            params["includeMovie"] = include_movie

        return self._get("queue/details", self.ver_uri, params)

    # GET /queue/status
    def get_queue_status(self) -> JsonObject:
        """Queue item status

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("queue/status", self.ver_uri)

    # DELETE /queue/bulk
    def del_queue_bulk(
        self,
        id_: list[int],
        remove_from_client: Optional[bool] = None,
        blocklist: Optional[bool] = None,
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Remove multiple items from queue by their IDs

        Args:
            id_ (list[int]): Dictionary of IDs to be removed::
            remove_from_client (bool, optional): Remove the items from the client. Defaults to True.
            blocklist (bool, optional): Add the items to the blocklist. Defaults to True.

        Returns:
            Response: HTTP Response
        """
        data = {"ids": id_}
        params = {"removeFromClient": remove_from_client, "blocklist": blocklist}
        return self._delete("queue/bulk", self.ver_uri, params=params, data=data)

    # POST /queue/grab/{id}
    def force_grab_queue_item(self, id_: int) -> JsonObject:
        """Perform a Radarr "force grab" on a pending queue item by its ID.

        Args:
            id_ (int): Queue item ID from database.

        Returns:
            JsonObject: Dictionary with record
        """
        return self._post(f"queue/grab/{id_}", self.ver_uri)

    ## COMMAND

    # POST /command
    def post_command(
        self, name: RadarrCommands, **kwargs: Optional[dict[str, Union[int, list[int]]]]
    ) -> JsonObject:
        """Performs any of the predetermined Radarr command routines.

        Args:
            name (RadarrCommands): Command that should be executed
            **kwargs: Additional parameters for specific commands. See note.

        Note:
            For available commands and required `**kwargs` see the `RadarrCommands` model


        Returns:
            JsonObject: Dictionary containing job
        """
        data: dict[str, Any] = {
            "name": name,
        }
        if kwargs:
            data |= kwargs
        return self._post("command", self.ver_uri, data=data)

    ## CUSTOM FILTERS

    # GET /customfilter
    def get_custom_filter(self) -> JsonArray:
        """Query Radarr for custom filters

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("customfilter", self.ver_uri)

    # POST /qualityprofile
    def add_quality_profile(
        self,
        name: str,
        schema: dict[str, Any],
        cutoff: int,
        upgrade_allowed: Optional[bool] = None,
        language: Optional[dict[str, Any]] = None,
        min_format_score: Optional[int] = None,
        cutoff_format_score: Optional[int] = None,
        format_items: Optional[list] = None,
    ) -> JsonObject:
        """Add new quality profile

        Args:
            name (str): Name of the profile
            schema (dict[str, Any]): Add the profile schema (from `get_quality_profile_schema()`)
            cutoff (int): ID of quality definition to cutoff at. Must be an allowed definition ID.
            upgrade_allowed (bool, optional): Are upgrades in quality allowed?. Default provided by schema.
            language (dict, optional): Language profile (from `get_language()`). Default provided by schema.
            min_format_score (int, optional): Minimum format score. Default provided by schema.
            cutoff_format_score (int, optional): Cutoff format score. Default provided by schema.
            format_items (list, optional): Format items. Default provided by schema.

        Note:
            Update the result from `get_quality_profile_schema()` set the items you need
            from `"allowed": false` to `"allowed": true`. See tests for more details.

        Returns:
            JsonObject: An object containing the profile
        """
        schema["name"] = name
        schema["cutoff"] = cutoff

        if format_items is not None:
            schema["formatItems"] = format_items
        if language is not None:
            schema["language"] = language
        if upgrade_allowed is not None:
            schema["upgradeAllowed"] = upgrade_allowed
        if min_format_score is not None:
            schema["minFormatScore"] = min_format_score
        if cutoff_format_score is not None:
            schema["cutoffFormatScore"] = cutoff_format_score

        return self._post("qualityprofile", self.ver_uri, data=schema)

    # GET /manualimport
    def get_manual_import(
        self,
        folder: str,
        download_id: Optional[str] = None,
        movie_id: Optional[int] = None,
        filter_existing_files: Optional[bool] = None,
        replace_existing_files: Optional[bool] = None,
    ) -> JsonArray:
        """Gets a manual import list

        Args:
            downloadId (str): Download IDs
            movieId (int, optional): Movie Database ID. Defaults to None.
            folder (Optional[str], optional): folder name. Defaults to None.
            filterExistingFiles (bool, optional): filter files. Defaults to True.
            replaceExistingFiles (bool, optional): replace files. Defaults to True.

        Returns:
            JsonArray: List of dictionaries with items
        """
        params: dict[str, Union[str, int, bool]] = {"folder": folder}
        if download_id:
            params["downloadId"] = download_id
        if movie_id:
            params["movieId"] = movie_id
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

    ## RELEASE

    # GET /release
    def get_release(self, id_: Optional[int] = None) -> JsonArray:
        """Query indexers for latest releases.

        Args:
            id_ (int): Database id for movie to check

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("release", self.ver_uri, {"movieId": id_} if id_ else None)

    # POST /release
    def post_release(self, guid: str, indexer_id: int) -> JsonObject:
        """Adds a previously searched release to the download client, if the release is
         still in Radarr's search cache (30 minute cache). If the release is not found
         in the cache Radarr will return a 404.

        Args:
            guid (str): Recently searched result guid
            indexer_id (int): Database id of indexer to use

        Returns:
            JsonObject: Dictionary with download release details
        """
        data = {"guid": guid, "indexerId": indexer_id}
        return self._post("release", self.ver_uri, data=data)

    # POST /release/push
    def post_release_push(
        self, title: str, download_url: str, protocol: str, publish_date: datetime
    ) -> Any:
        """If the title is wanted, Radarr will grab it.

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
