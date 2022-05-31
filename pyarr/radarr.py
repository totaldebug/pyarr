from typing import Any, Optional

from requests import Response

from .base import BaseArrAPI
from .const import PAGE, PAGE_SIZE
from .exceptions import PyarrRecordNotFound
from .models.common import PyarrSortDirection
from .models.radarr import RadarrCommands, RadarrSortKeys


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
        db_id: str,
        quality_profile_id: int,
        root_dir: str,
        monitored: bool = True,
        search_for_movie: bool = True,
        tmdb: bool = True,
    ) -> dict[str, Any]:
        """Searches for movie on tmdb and returns Movie json to add.

        Args:
            db_id (str): imdb or tmdb id
            quality_profile_id (int): ID of the quality profile the movie will use
            root_dir (str): location of the root DIR
            monitored (bool, optional): should the movie be monitored. Defaults to True.
            search_for_movie (bool, optional): Should we search for the movie. Defaults to True.
            tmdb (bool, optional): Use TMDB IDs. Set to False to use IMDB. Defaults to True.

        Raises:
            PyarrRecordNotFound: Movie doesnt exist

        Returns:
            dict[str, Any]: Dictionary containing movie information
        """
        if tmdb:
            movie = self.lookup_movie_by_tmdb_id(db_id)[0]
        else:
            movie = self.lookup_movie_by_imdb_id(db_id)[0]

        if not movie:
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

    ## MOVIE

    # GET /movie
    def get_movie(
        self, id_: Optional[int] = None
    ) -> list[dict[str, Any]]:  # sourcery skip: class-extract-method
        """Returns all movies in the database, or returns a movie with a specific TMDB ID.

        Args:
            id_ (int, optional): TMDB Id of Movies. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of Dictionaries with items
        """
        params = {}
        if id_:
            params["tmdbId"] = id_
        path = "movie"
        return self.assert_return(path, self.ver_uri, list, params)

    # POST /movie
    def add_movie(
        self,
        db_id: str,
        quality_profile_id: int,
        root_dir: str,
        monitored: bool = True,
        search_for_movie: bool = True,
        tmdb: bool = True,
    ) -> dict[str, Any]:
        """Adds a movie to the database

        Args:
            db_id (str): IMDB or TMDB ID
            quality_profile_id (int): ID of the quality profile the movie will use
            root_dir (str): Location of the root DIR
            monitored (bool, optional): Should the movie be monitored. Defaults to True.
            search_for_movie (bool, optional): Should we search for the movie. Defaults to True.
            tmdb (bool, optional): Use TMDB IDs. Set to False to use IMDB. Defaults to True.

        Returns:
            dict[str, Any]: Dictonary with added record
        """
        movie_json = self._movie_json(
            db_id, quality_profile_id, root_dir, monitored, search_for_movie, tmdb
        )

        return self._post("movie", self.ver_uri, data=movie_json)

    # PUT /movie
    def upd_movie(
        self, data: dict[str, Any], move_files: bool = False
    ) -> dict[str, Any]:
        """Updates a movie in the database.

        Args:
            data (dict[str, Any]): Dictionary containing an object obtained from get_movie()
            move_files (bool, optional): Have radarr move files when updating. Defaults to False.

        Returns:
            dict[str, Any]: Dictionary with updated record
        """
        params = {"moveFiles": move_files}
        return self._put("movie", self.ver_uri, data=data, params=params)

    # GET /movie/{id}
    def get_movie_by_movie_id(self, id_: int) -> list[dict[str, Any]]:
        """Get a movie by the Radarr database ID

        Args:
            id_ (int): Database Id of movie to return

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return(f"movie/{id_}", self.ver_uri, list)

    # DELETE /movie/{id}
    def del_movie(
        self, id_: int, delete_files: bool = False, add_exclusion: bool = False
    ) -> Response:
        """Delete a single movie by database id.

        Args:
            id_ (int): Database Id of movie to delete.
            delete_files (bool, optional): Delete movie files when deleting movies. Defaults to False.
            add_exclusion (bool, optional): Add deleted movies to List Exclusions. Defaults to False.

        Returns:
            Response: HTTP Response
        """
        params = {"deleteFiles": delete_files, "addExclusion": add_exclusion}
        return self._delete(f"movie/{id_}", self.ver_uri, params=params)

    # GET /movie/lookup
    def lookup_movie(self, term: str) -> list[dict[str, Any]]:
        """Search for a movie to add to the database (Uses TMDB for search results)

        Args:
            term (str): Search term to use for lookup

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {"term": term}
        return self.assert_return("movie/lookup", self.ver_uri, list, params)

    # GET /movie/lookup
    def lookup_movie_by_tmdb_id(self, id_: str) -> list[dict[str, Any]]:
        """Search for movie by TMDB ID

        Args:
            id_ (str): TMDB ID

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
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
        return self._put("movie/editor", self.ver_uri, data=data)

    # DELETE /movie/editor
    def del_movies(self, data: dict[str, Any]) -> Response:
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
    def get_movie_files(self, moviefile_ids: list[int]) -> list[dict[str, Any]]:
        """Get movie file information for multiple movie files

        Args:
            moviefile_ids (list[int]): a list of movie file IDs

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {"moviefileids": moviefile_ids}
        return self.assert_return("moviefile", self.ver_uri, list, params)

    # GET /moviefile/{id}
    def get_movie_file(self, id_: int) -> list[dict[str, Any]]:
        """Get movie file by database ID

        Args:
            id_ (int): Movie file ID

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return(f"moviefile/{id_}", self.ver_uri, list)

    # DELETE /moviefile/{id}
    def del_movie_file(self, id_: int) -> Response:
        """Allows for deletion of a moviefile by its database ID.

        Args:
            id_ (int): Movie file ID

        Returns:
            Response: HTTP Response
        """
        return self._delete(
            f"moviefile/{id_}",
            self.ver_uri,
        )

    # GET /history/movie
    def get_movie_history(
        self, id_: int, event_type: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """Get history for a given movie in database by its database ID

        Args:
            id_ (int): Database ID of movie
            event_type (int, optional): History event type to retrieve. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {"movieId": id_}
        if event_type:
            params["eventType"] = event_type
        return self.assert_return("history/movie", self.ver_uri, list, params)

    ## BLACKLIST

    # GET /blacklist/movie
    def get_blacklist_by_movie_id(
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
        return self.assert_return("blacklist/movie", self.ver_uri, list, params)

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_direction: PyarrSortDirection = PyarrSortDirection.ASC,
        sort_key: RadarrSortKeys = RadarrSortKeys.TIMELEFT,
        include_unknown_movie_items: bool = True,
    ) -> dict[str, Any]:
        """Return a list of items in the queue

        Args:
            page (int, optional): Page to be returned. Defaults to PAGE.
            page_size (int, optional): Number of results per page. Defaults to PAGE_SIZE.
            sort_direction (PyarrSortDirection, optional): Direction to sort. Defaults to PyarrSortDirection.ASC.
            sort_key (RadarrSortKeys, optional): Field to sort. Defaults to RadarrSortKeys.TIME.
            include_unknown_movie_items (bool, optional): Include unknown movie items. Defaults to True.

        Returns:
            dict[str, Any]: List of dictionaries with items
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortDirection": sort_direction,
            "sortKey": sort_key,
            "includeUnknownMovieItems": include_unknown_movie_items,
        }
        return self.assert_return("queue", self.ver_uri, dict, params)

    # DELETE /queue/bulk
    def del_queue_bulk(
        self,
        data: dict[str, Any],
        remove_from_client: bool = True,
        blacklist: bool = True,
    ) -> Response:
        """Remove multiple items from queue by their IDs

        Args:
            data (dict[str, Any]): Dictionary of IDs to be removed::

                {
                "ids": [
                    0
                ]
                }

            remove_from_client (bool, optional): Remove the items from the client. Defaults to True.
            blacklist (bool, optional): Add the items to the blacklist. Defaults to True.

        Returns:
            Response: HTTP Response
        """
        params = {"removeFromClient": remove_from_client, "blacklist": blacklist}
        return self._delete("queue/bulk", self.ver_uri, params=params, data=data)

    # GET /queue/details
    def get_queue_details(
        self,
        include_movie: bool = True,
    ) -> list[dict[str, Any]]:
        """Get details of all items in queue

        Args:
            include_movie (bool, optional): Include movie object if linked. Defaults to True.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {
            "includeMovie": include_movie,
        }
        return self.assert_return("queue/details", self.ver_uri, list, params)

    # GET /queue/status
    def get_queue_status(self) -> list[dict[str, Any]]:
        """Queue item status

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("queue/status", self.ver_uri, list)

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
        return self.assert_return(path, self.ver_uri, list)

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
    def del_indexer(self, id_: int) -> Response:
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
    def post_command(self, name: RadarrCommands, **kwargs) -> Any:
        """Performs any of the predetermined Radarr command routines.

        Args:
            name (RadarrCommands): Name of the command to be run
            **kwargs: additional parameters for specific commands

        Returns:
            JSON: Array
        """
        data = {
            "name": name,
            **kwargs,
        }
        return self._post("command", self.ver_uri, data=data)

    ## CUSTOM FILTERS

    # GET /customfilter
    def get_custom_filter(self) -> list[dict[str, Any]]:
        """Query Radarr for custom filters

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("customfilter", self.ver_uri, list)
