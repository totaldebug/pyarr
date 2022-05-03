from .base import BaseArrAPI
from .const import PAGE, PAGE_SIZE


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
        db_id,
        quality_profile_id,
        root_dir,
        monitored=True,
        search_for_movie=True,
        tmdb=True,
    ):
        """Searches for movie on tmdb and returns Movie json to add.

        Args:
            db_id (str): imdb or tmdb id
            quality_profile_id (int): ID of the quality profile the movie will use
            root_dir (str): location of the root DIR
            monitored (bool, optional): should the movie be monitored. Defaults to True.
            search_for_movie (bool, optional): Should we search for the movie. Defaults to True.
            tmdb (bool, optional): Use TMDB IDs. Set to False to use IMDB. Defaults to True.

        Raises:
            Exception: [description]

        Returns:
            JSON: Movie JSON for adding a movie to radarr
        """
        if tmdb:
            movie = self.lookup_movie_by_tmdb_id(db_id)[0]
        else:
            movie = self.lookup_movie_by_imdb_id(db_id)[0]

        if not movie:
            raise Exception("Movie Doesn't Exist")

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
    def get_movie(self, id_=None):  # sourcery skip: class-extract-method
        """Returns all movies in the database, or returns a movie with a specific TMDB ID.

        Args:
            id_ (int, optional): TMDB Id of Movies. Defaults to None.

        Returns:
            JSON: List of Movies from Radarr database
        """
        params = {}
        if id_:
            params["tmdbId"] = id_
        path = "movie"
        return self.request_get(path, self.ver_uri, params=params)

    # POST /movie
    def add_movie(
        self,
        db_id,
        quality_profile_id,
        root_dir,
        monitored=True,
        search_for_movie=True,
        tmdb=True,
    ):
        """Adds a movie to the database

        Args:
            db_id (str): IMDB or TMDB ID
            quality_profile_id (int): ID of the quality profile the movie will use
            root_dir (str): location of the root DIR
            monitored (bool, optional): should the movie be monitored. Defaults to True.
            search_for_movie (bool, optional): Should we search for the movie. Defaults to True.
            tmdb (bool, optional): Use TMDB IDs. Set to False to use IMDB. Defaults to True.

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        movie_json = self._movie_json(
            db_id, quality_profile_id, root_dir, monitored, search_for_movie, tmdb
        )

        path = "movie"
        return self.request_post(path, self.ver_uri, data=movie_json)

    # PUT /movie
    def upd_movie(self, data, move_files=False):
        """Updates a movie in the database.

        Args:
            data (dict): Dictionary containing an object obtained from get_movie()
            move_files (bool, optional): Have radarr move files when updating. Defaults to False.

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """

        path = "movie"
        params = {"moveFiles": move_files}
        return self.request_put(path, self.ver_uri, data=data, params=params)

    # GET /movie/{id}
    def get_movie_by_movie_id(self, id_):
        """Get a movie by the Radarr database ID

        Args:
            id_ (int): Database Id of movie to return

        Returns:
            JSON: Movie data if present in database
        """
        path = f"movie/{id_}"
        return self.request_get(path, self.ver_uri)

    # DELETE /movie/{id}
    def del_movie(self, id_, delete_files=False, add_exclusion=False):
        """Delete a single movie by database id.

        Args:
            id_ (int): Database Id of movie to delete.
            delete_files (bool, optional): Delete movie files when deleting movies. Defaults to False.
            add_exclusion (bool, optional): Add deleted movies to List Exclusions. Defaults to False.

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        params = {"deleteFiles": delete_files, "addExclusion": add_exclusion}
        path = f"movie/{id_}"
        return self.request_del(path, self.ver_uri, params=params)

    # GET /movie/lookup
    def lookup_movie(self, term):
        """Search for a movie to add to the database (Uses TMDB for search results)

        Args:
            term (str): search term to use for lookup

        Returns:
            JSON: List of movies found
        """
        params = {"term": term}
        path = "movie/lookup"
        return self.request_get(path, self.ver_uri, params=params)

    # GET /movie/lookup
    def lookup_movie_by_tmdb_id(self, id_):
        """Search for movie by TMDB ID

        Args:
            id_ (str): TMDB ID

        Returns:
            JSON: List of movies found
        """
        params = {"term": f"tmdb:{id_}"}
        path = "movie/lookup"
        return self.request_get(path, self.ver_uri, params=params)

    # GET /movie/lookup
    def lookup_movie_by_imdb_id(self, id_):
        """Search for movie by IMDB ID

        Args:
            id_ (str): IMDB ID

        Returns:
            JSON: List of movies found
        """
        params = {"term": f"imdb:{id_}"}
        path = "movie/lookup"
        return self.request_get(path, self.ver_uri, params=params)

    # PUT /movie/editor
    def upd_movies(self, data):
        """The Updates operation allows to edit properties of multiple movies at once

        Args:
            data (dict): Updated movie information

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "movie/editor"
        return self.request_put(path, self.ver_uri, data=data)

    # DELETE /movie/editor
    def del_movies(self, data):
        """The delete operation allows mass deletion of movies (and optionally files)

        Args:
            data (dict): dictionary of movies to be deleted::

                {
                    "movieIds": [
                        0
                    ],
                    "deleteFIles": true,
                    "addImportExclusion": true
                }

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "movie/editor"
        return self.request_del(path, self.ver_uri, data=data)

    # POST /movie/import
    def import_movies(self, data):
        """The movie import endpoint is used by the bulk import view in Radarr UI. It allows movies to be bulk added to the Radarr database.

        Args:
            data (dict): dictionary of all movies to be imported

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "movie/import"
        return self.request_post(path, self.ver_uri, data=data)

    ## MOVIEFILE

    # GET /moviefile
    def get_movie_files_by_movie_id(self, id_):
        """Get a movie file object by Movie database id.

        Args:
            id_ (int): Movie database id

        Returns:
            JSON: Movie file information if exists
        """
        params = {"movieid": id_}
        path = "moviefile"
        return self.request_get(path, self.ver_uri, params=params)

    # GET /moviefile
    def get_movie_files(self, moviefile_ids):
        """Get movie file information for multiple movie files

        Args:
            moviefile_ids (array): an array of movie file ids

        Returns:
            JSON: List of movie files
        """
        params = {"moviefileids": moviefile_ids}
        path = "moviefile"
        return self.request_get(path, self.ver_uri, params=params)

    # GET /moviefile/{id}
    def get_movie_file(self, id_):
        """Get movie file by database id

        Args:
            id_ (int): movie file id

        Returns:
            JSON: movie file information
        """
        path = f"moviefile/{id_}"
        return self.request_get(path, self.ver_uri)

    # DELETE /moviefile/{id}
    def del_movie_file(self, id_):
        """Allows for deletion of a moviefile by its database id.

        Args:
            id_ (int): Movie file id

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"moviefile/{id_}"
        return self.request_del(
            path,
            self.ver_uri,
        )

    # GET /history/movie
    def get_movie_history(self, id_, event_type=None):
        """Get history for a given movie in database by its database id

        Args:
            id_ (int): Database id of movie
            event_type (int, optional): History event type to retrieve. Defaults to None.

        Returns:
            JSON: Array
        """
        params = {"movieId": id_}
        if event_type:
            params["eventType"] = event_type
        path = "history/movie"
        return self.request_get(path, self.ver_uri, params=params)

    ## BLACKLIST

    # GET /blacklist/movie
    def get_blacklist_by_movie_id(
        self,
        id_,
    ):
        """Retrieves blacklisted releases that are tied to a given movie in the database.

        Args:
            id_ (int): Movie id from Database

        Returns:
            JSON: Array
        """
        params = {"movieId": id_}
        path = "blacklist/movie"
        return self.request_get(path, self.ver_uri, params=params)

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page=PAGE,
        page_size=PAGE_SIZE,
        sort_direction="ascending",
        sort_key="timeLeft",
        include_unknown_movie_items=True,
    ):
        """Return a json object list of items in the queue

        Args:
            page (int, optional): Page to be returned. Defaults to 1.
            page_size (int, optional): Number of results per page. Defaults to 20.
            sort_direction (str, optional): Direction to sort items. Defaults to "ascending".
            sort_key (str, optional): Field to sort by. Defaults to "timeLeft".
            include_unknown_movie_items (bool, optional): Include unknown movie items. Defaults to True.

        Returns:
            JSON: Array
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortDirection": sort_direction,
            "sortKey": sort_key,
            "includeUnknownMovieItems": include_unknown_movie_items,
        }
        path = "queue"
        return self.request_get(path, self.ver_uri, params=params)

    # DELETE /queue/bulk
    def del_queue_bulk(self, data, remove_from_client=True, blacklist=True):
        """Remove multiple items from queue by their ids

        Args:
            data (dict): Dictionary of IDs to be removed::

                {
                "ids": [
                    0
                ]
                }

            remove_from_client (bool, optional): Remove the items from the client. Defaults to True.
            blacklist (bool, optional): Add the items to the blacklist. Defaults to True.

        Returns:
            JSON: 200 ok, 401 invalid api key
        """
        params = {"removeFromClient": remove_from_client, "blacklist": blacklist}
        path = "queue/bulk"
        return self.request_del(path, self.ver_uri, params=params, data=data)

    # GET /queue/details
    def get_queue_details(
        self,
        include_movie=True,
    ):
        """Get details of all items in queue

        Args:
            include_movie (bool, optional): Include movie object if linked. Defaults to True.

        Returns:
            JSON: Array
        """
        params = {
            "includeMovie": include_movie,
        }
        path = "queue/details"
        return self.request_get(path, self.ver_uri, params=params)

    # GET /queue/status
    def get_queue_status(self):
        """Stats on items in queue

        Returns:
            JSON: Array
        """
        path = "queue/status"
        return self.request_get(path, self.ver_uri)

    # POST /queue/grab/{id}
    def force_grab_queue_item(self, id_):
        """Perform a Radarr "force grab" on a pending queue item by its ID.

        Args:
            id_ (int): queue item id from database.

        Returns:
            JSON: 200 ok, 401 Invalid API Key
        """
        path = f"queue/grab/{id_}"
        return self.request_post(path, self.ver_uri)

    ## INDEXER

    # GET /indexer and /indexer/{id}
    def get_indexer(self, id_=None):
        """Get all indexers or a single indexer by its database id.

        Args:
            id_ (int, optional): indexer database id. Defaults to None.

        Returns:
            JSON: Array
        """
        path = f"indexer/{id_}" if id_ else "indexer"
        return self.request_get(path, self.ver_uri)

    # PUT /indexer/{id}
    def upd_indexer(self, id_, data):
        """Edit an indexer

        Args:
            id_ (int): Database id of indexer
            data (dict): information to be changed within the indexer

        Returns:
            JSON: 200 ok, 401 Unauthorized
        """
        path = f"indexer/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    # DELETE /indexer/{id}
    def del_indexer(self, id_):
        """Delete indexer by database id

        Args:
            id_ (int): DAtabase id of the indexer

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"indexer/{id_}"
        return self.request_del(path, self.ver_uri)

    ## COMMAND

    # POST /command
    def post_command(self, name, **kwargs):
        """Performs any of the predetermined Radarr command routines.

        Note:
            For command names and kwargs:
            See https://radarr.video/docs/api/#/Command/post-command

        Args:
            name (str): Name of the command to be run
            **kwargs: additional parameters for specific commands

        Returns:
            JSON: Array
        """
        data = {
            "name": name,
            **kwargs,
        }
        path = "command"
        return self.request_post(path, self.ver_uri, data=data)

    ## CUSTOM FILTERS

    # GET /customfilter
    def get_custom_filter(self):
        """Query Radarr for custom filters

        Returns:
            JSON: Array
        """
        path = "customfilter"
        return self.request_get(path, self.ver_uri)
