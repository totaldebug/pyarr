from typing import Any, Optional, Union
from warnings import warn

from requests import Response

from .base import BaseArrAPI
from .exceptions import PyarrMissingArgument, PyarrRecordNotFound
from .models.common import PyarrSortDirection
from .models.radarr import RadarrCommands, RadarrEventType, RadarrSortKeys


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

    def _movie_json(
        self,
        id_: Union[str, int],
        quality_profile_id: int,
        root_dir: str,
        monitored: bool = True,
        search_for_movie: bool = True,
        tmdb: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Searches for movie on tmdb and returns Movie json to add.

        Args:
            id_ (Union[str, int]): imdb or tmdb id
            quality_profile_id (int): ID of the quality profile the movie will use
            root_dir (str): location of the root DIR
            monitored (bool, optional): should the movie be monitored. Defaults to True.
            search_for_movie (bool, optional): Should we search for the movie. Defaults to True.
            tmdb (bool, optional): Not used, deprecated. Defaults to True.

        Raises:
            PyarrRecordNotFound: Movie doesnt exist

        Returns:
            dict[str, Any]: Dictionary containing movie information
        """
        if tmdb is not None:
            warn(
                "Argument tmdb is no longer used and will be removed in a future release.",
                DeprecationWarning,
                stacklevel=2,
            )
        if isinstance(id_, int):
            movies = self.lookup_movie(term=f"tmdb:{id_}")
        else:
            movies = self.lookup_movie(term=f"imdb:{id_}")
        if movies:
            movie = movies[0]
        if not movies:
            raise PyarrRecordNotFound("Movie Doesn't Exist")

        return {
            "title": movie["title"],
            "rootFolderPath": root_dir,
            "qualityProfileId": quality_profile_id,
            "year": movie["year"],
            "tmdbId": movie["tmdbId"],
            "images": movie["images"],
            "titleSlug": movie["titleSlug"],
            "monitored": monitored,
            "addOptions": {"searchForMovie": search_for_movie},
        }

    ## CONFIG
    # POST /rootfolder
    def add_root_folder(
        self,
        directory: str,
    ) -> dict[str, Any]:
        """Adds a new root folder

        Args:
            directory (str): The directory path

        Returns:
            dict[str, Any]: Dictionary containing path details
        """
        return self._post("rootfolder", self.ver_uri, data={"path": directory})

    ## MOVIE

    # GET /movie
    def get_movie(
        self, id_: Optional[int] = None, tmdb: bool = False
    ) -> Union[
        list[dict[str, Any]], dict[str, Any]
    ]:  # sourcery skip: class-extract-method
        """Returns all movies in the database, movie based on the Radarr ID or TMDB id.

        Note:
            IMDB is not supported at this time

        Args:
            id_ (Optional[int], optional): Radarr ID or TMDB ID of Movies. Defaults to None.
            tmdb (bool): Use TMDB Id. Defaults to False

        Returns:
            Union[list[dict[str, Any]], dict[str, Any]]: List or Dictionary with items
        """
        params = {}
        if tmdb:
            params["tmdbid"] = id_

        return self.assert_return(
            f"movie{'' if id_ is None or tmdb else f'/{id_}'}",
            self.ver_uri,
            dict if id_ and not tmdb else list,
            params=params,
        )

    # POST /movie
    def add_movie(
        self,
        id_: Union[str, int],
        quality_profile_id: int,
        root_dir: str,
        monitored: bool = True,
        search_for_movie: bool = True,
        tmdb: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Adds a movie to the database

        Args:
            id_ (Union[str, int]): IMDB or TMDB ID
            quality_profile_id (int): ID of the quality profile the movie will use
            root_dir (str): Location of the root DIR
            monitored (bool, optional): Should the movie be monitored. Defaults to True.
            search_for_movie (bool, optional): Should we search for the movie. Defaults to True.
            tmdb (Optional[bool], optional): Not in use, Deprecated. Defaults to None.

        Returns:
            dict[str, Any]: Dictonary with added record
        """

        if tmdb:
            warn(
                "Argument tmdb is no longer used and will be removed in a future release.",
                DeprecationWarning,
                stacklevel=2,
            )
        movie_json = self._movie_json(
            id_, quality_profile_id, root_dir, monitored, search_for_movie
        )

        return self._post("movie", self.ver_uri, data=movie_json)

    # PUT /movie
    def upd_movie(
        self,
        data: Optional[dict[Any, Any]],
        move_files: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Updates a movie in the database.

        Args:
            data (dict[str, Any]): Dictionary containing an object obtained from get_movie()
            move_files (Optional[bool], optional): Have radarr move files when updating. Defaults to None.

        Returns:
            dict[str, Any]: Dictionary with updated record
        """
        params = {}
        if move_files is not None:
            params["moveFiles"] = move_files

        return self._put(
            f"movie{'/editor' if isinstance(data, list) else ''}",
            self.ver_uri,
            data=data,
            params=params,
        )

    # GET /movie/{id}
    def get_movie_by_movie_id(self, id_: int) -> dict[str, Any]:
        """Get a movie by the Radarr database ID

        Args:
            id_ (int): Database Id of movie to return

        Note:
            This method is deprecated and will be removed in a
            future release. Please use get_movie()

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. Please use get_movie()",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.assert_return(f"movie/{id_}", self.ver_uri, dict)

    # DELETE /movie/{id}
    def del_movie(
        self,
        id_: Union[int, list],
        delete_files: Optional[bool] = None,
        add_exclusion: Optional[bool] = None,
    ) -> Union[Response, dict[str, Any], dict[Any, Any]]:
        """Delete a single movie or multiple movies by database id.

        Args:
            id_ (Union[int, list]): Int with single movie Id or list with multiple IDs to delete.
            delete_files (bool, optional): Delete movie files when deleting movies. Defaults to None.
            add_exclusion (bool, optional): Add deleted movies to List Exclusions. Defaults to None.

        Returns:
            Response: HTTP Response
        """
        params: dict[str, Union[str, list[int], int]] = {}
        if delete_files:
            params["deleteFiles"] = str(delete_files)

        if add_exclusion:
            params["addImportExclusion"] = str(add_exclusion)

        if isinstance(id_, list):
            params["movieIds"] = id_
        return self._delete(
            "movie/editor" if isinstance(id_, list) else f"movie/{id_}",
            self.ver_uri,
            params=None if isinstance(id_, list) else params,
            data=params if isinstance(id_, list) else None,
        )

    # GET /movie/lookup
    def lookup_movie(self, term: str) -> list[dict[str, Any]]:
        """Search for a movie to add to the database (Uses TMDB for search results)

        Args:
            term (str): Search term to use for lookup, can also do IMDB & TMDB IDs::

                radarr.lookup_movie(term="imdb:123456")
                radarr.lookup_movie(term="tmdb:123456")

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {"term": term}
        return self.assert_return("movie/lookup", self.ver_uri, list, params)

    # GET /movie/lookup
    def lookup_movie_by_tmdb_id(self, id_: int) -> list[dict[str, Any]]:
        """Search for movie by TMDB ID

        Args:
            id_ (str): TMDB ID

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. use lookup_movie(term='tmdb:123456')",
            DeprecationWarning,
            stacklevel=2,
        )
        params = {"term": f"tmdb:{id_}"}
        return self.assert_return("movie/lookup", self.ver_uri, list, params)

    # GET /movie/lookup
    def lookup_movie_by_imdb_id(self, id_: str) -> list[dict[str, Any]]:
        """Search for movie by IMDB ID

        Args:
            id_ (str): IMDB ID

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        warn(
            "This method is deprecated and will be removed in a future release. use lookup_movie(term='imdb:123456')",
            DeprecationWarning,
            stacklevel=2,
        )
        params = {"term": f"imdb:{id_}"}
        return self.assert_return("movie/lookup", self.ver_uri, list, params)

    # PUT /movie/editor
    def upd_movies(self, data: dict[str, Any]) -> dict[str, Any]:
        """The Updates operation allows to edit properties of multiple movies at once

        Args:
            data (dict[str, Any]): Updated movie information

        Returns:
            dict[str, Any]: Dictionary containing updated record
        """

        warn(
            "This method is deprecated and will be removed in a future release. Please use upd_movie() with a list to update",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._put("movie/editor", self.ver_uri, data=data)

    # DELETE /movie/editor
    def del_movies(
        self, data: dict[str, Any]
    ) -> Union[Response, dict[str, Any], dict[Any, Any]]:
        """The delete operation allows mass deletion of movies (and optionally files)

        Args:
            data (dict[str, Any]): dictionary of movies to be deleted::

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
            "This method is deprecated and will be removed in a future release. Please use del_movie().",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._delete("movie/editor", self.ver_uri, data=data)

    # POST /movie/import
    def import_movies(self, data: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """The movie import endpoint is used by the bulk import view in Radarr UI. It allows movies to be bulk added to the Radarr database.

        Args:
            data (dict[str, Any]): dictionary of all movies to be imported

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        response = self._post("movie/import", self.ver_uri, data=data)
        assert isinstance(response, list)
        return response

    ## MOVIEFILE

    # GET /moviefile
    # TODO: merge this with get_movie_file
    def get_movie_files_by_movie_id(self, id_: int) -> list[dict[str, Any]]:
        """Get a movie file object by Movie database ID.

        Args:
            id_ (int): Movie database ID

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """

        params = {"movieid": id_}
        return self.assert_return("moviefile", self.ver_uri, list, params)

    # GET /moviefile
    def get_movie_file(self, id_: Union[int, list]) -> list[dict[str, Any]]:
        """Get movie file by database ID

        Args:
            id_ (int, list): Movie file ID, or multiple in a list

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        if not isinstance(id_, list):
            return self.assert_return(
                f"moviefile/{id_}",
                self.ver_uri,
                dict,
            )
        params = [("movieFileIds", file) for file in id_]
        return self.assert_return("moviefile", self.ver_uri, list, params=params)

    # DELETE /moviefile/{id}
    def del_movie_file(
        self, id_: Union[int, list]
    ) -> Union[Response, dict[str, Any], dict[Any, Any]]:
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
    ) -> list[dict[str, Any]]:
        """Get history for a given movie in database by its database ID

        Args:
            id_ (int): Database ID of movie
            event_type (Optional[RadarrEventType], optional): History event type to retrieve. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params: dict[str, Union[int, str]] = {"movieId": id_}
        if event_type:
            params["eventType"] = event_type
        return self.assert_return("history/movie", self.ver_uri, list, params)

    ## BLACKLIST

    # GET /blacklist/movie
    def get_blocklist_by_movie_id(
        self,
        id_: int,
    ) -> list[dict[str, Any]]:
        """Retrieves blacklisted releases that are tied to a given movie in the database.

        Args:
            id_ (int): Movie id from Database

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {"movieId": id_}
        return self.assert_return("blocklist/movie", self.ver_uri, list, params)

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
        sort_key: Optional[RadarrSortKeys] = None,
        include_unknown_movie_items: Optional[bool] = None,
    ) -> dict[str, Any]:
        """Return a list of items in the queue

        Args:
            page (Optional[int], optional): Page to be returned. Defaults to None.
            page_size (Optional[int], optional): Number of results per page. Defaults to None.
            sort_direction (Optional[PyarrSortDirection], optional): Direction to sort. Defaults to None.
            sort_key (Optional[RadarrSortKeys], optional): Field to sort. Defaults to None.
            include_unknown_movie_items (Optional[bool], optional): Include unknown movie items. Defaults to None.

        Returns:
            dict[str, Any]: List of dictionaries with items
        """
        params: dict[str, Union[int, PyarrSortDirection, RadarrSortKeys, bool]] = {}

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

        return self.assert_return("queue", self.ver_uri, dict, params)

    # GET /queue/details
    def get_queue_details(
        self,
        id_: Optional[int] = None,
        include_movie: Optional[bool] = None,
    ) -> list[dict[str, Any]]:
        """Get details of all items in queue

        Args:
            id_ (Optional[int], optional): select specific item by id. Defaults to None
            include_movie (Optional[bool], optional): Include movie object if linked. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {}
        if id_:
            params["movieId"] = id_
        if include_movie is not None:
            params["includeMovie"] = include_movie

        return self.assert_return("queue/details", self.ver_uri, list, params)

    # GET /queue/status
    def get_queue_status(self) -> dict[str, Any]:
        """Queue item status

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("queue/status", self.ver_uri, dict)

    # DELETE /queue/bulk
    def del_queue_bulk(
        self,
        id_: list[int],
        remove_from_client: Optional[bool] = None,
        blocklist: Optional[bool] = None,
    ) -> Union[Response, dict[str, Any], dict[Any, Any]]:
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
    def force_grab_queue_item(self, id_: int) -> dict[str, Any]:
        """Perform a Radarr "force grab" on a pending queue item by its ID.

        Args:
            id_ (int): Queue item ID from database.

        Returns:
            dict[str, Any]: Dictionary with record
        """
        return self._post(f"queue/grab/{id_}", self.ver_uri)

    ## INDEXER

    # GET /indexer and /indexer/{id}
    def get_indexer(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Get all indexers or a single indexer by its database ID.

        Args:
            id_ (Optional[int], optional): indexer database ID. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"indexer/{id_}" if id_ else "indexer"
        return self.assert_return(path, self.ver_uri, dict if id_ else list)

    # PUT /indexer/{id}
    def upd_indexer(self, id_: int, data: dict[str, Any]) -> dict[str, Any]:
        """Edit an indexer

        Args:
            id_ (int): Database ID of indexer
            data (dict[str, Any]): information to be changed within the indexer

        Returns:
            dict[str, Any]: Dictionary with updated record
        """
        return self._put(f"indexer/{id_}", self.ver_uri, data=data)

    # DELETE /indexer/{id}
    def del_indexer(self, id_: int) -> Union[Response, dict[str, Any], dict[Any, Any]]:
        """Delete indexer by database ID

        Args:
            id_ (int): DAtabase ID of the indexer

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"indexer/{id_}", self.ver_uri)

    ## COMMAND

    # POST /command
    # TODO: type for kwargs and response
    def post_command(
        self, name: RadarrCommands, **kwargs: Optional[Union[int, list[int]]]
    ) -> dict[str, Any]:
        """Performs any of the predetermined Radarr command routines.

        Args:
            name (SonarrCommands): Command that should be executed
            **kwargs: Additional parameters for specific commands. See note.

        Note:
            Required Kwargs:
                DownloadedMoviesScan: clientid (int, Optional)
                RenameFiles: files (list[int])
                DownloadedMoviesScan: path (str, Optional)
                MissingMoviesSearch
                RefreshMovie: movieid (Optional)
                RenameMovie: movieid (list[int])
                RescanMovie: movieid (Optional)
                MovieSearch: movieid (Optional)

        Returns:
            dict[str, Any]: Dictionary containing job
        """
        data: dict[str, Any] = {
            "name": name,
        }
        if kwargs:
            data |= kwargs
        return self._post("command", self.ver_uri, data=data)

    ## CUSTOM FILTERS

    # GET /customfilter
    def get_custom_filter(self) -> list[dict[str, Any]]:
        """Query Radarr for custom filters

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("customfilter", self.ver_uri, list)
