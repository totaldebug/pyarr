from .request_api import RequestAPI


class RadarrAPI(RequestAPI):
    """API wrapper for Radarr endpoints.

    Args:
        RequestAPI (:obj:`str`): provides connection to API endpoint
    """

    def _construct_movie_json(
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

        movie_json = {
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
        return movie_json

    ## MOVIE

    # GET /movie
    def get_movie(self, id_=None):
        """Returns all movies in the database, or returns a movie with a specific TMDB ID.

        Args:
            id_ (int, optional): TMDB Id of Movies. Defaults to None.

        Returns:
            JSON: List of Movies from Radarr database
        """
        params = {}
        if id_:
            params["tmdbId"] = id_
        path = "/api/v3/movie"
        res = self.request_get(path, params=params)
        return res

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
        movie_json = self._construct_movie_json(
            db_id, quality_profile_id, root_dir, monitored, search_for_movie, tmdb
        )

        path = "/api/v3/movie"
        res = self.request_post(path, data=movie_json)
        return res

    # PUT /movie
    def upd_movie(self, data, move_files=False):
        """Updates a movie in the database.

        Args:
            data (dict): Dictionary containing an object obtained from get_movie()
            move_files (bool, optional): Have radarr move files when updating. Defaults to False.

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """

        path = "/api/movie"
        params = {"moveFiles": move_files}
        res = self.request_put(path, data=data, params=params)
        return res

    # GET /movie/{id}
    def get_movie_by_movie_id(self, id_):
        """Get a movie by the Radarr database ID

        Args:
            id_ (int): Database Id of movie to return

        Returns:
            JSON: Movie data if present in database
        """
        path = f"/api/v3/movie/{id_}"
        res = self.request_get(path)
        return res

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
        path = f"/api/v3/movie/{id_}"
        res = self.request_del(path, params=params)
        return res

    # GET /movie/lookup
    def lookup_movie(self, term):
        """Search for a movie to add to the database (Uses TMDB for search results)

        Args:
            term (str): search term to use for lookup

        Returns:
            JSON: List of movies found
        """
        params = {"term": term}
        path = "/api/v3/movie/lookup"
        res = self.request_get(path, params=params)
        return res

    # GET /movie/lookup
    def lookup_movie_by_tmdb_id(self, id_):
        """Search for movie by TMDB ID

        Args:
            id_ (str): TMDB ID

        Returns:
            JSON: List of movies found
        """
        params = {"term": f"tmdb:{id_}"}
        path = "/api/v3/movie/lookup"
        res = self.request_get(path, params=params)
        return res

    # GET /movie/lookup
    def lookup_movie_by_imdb_id(self, id_):
        """Search for movie by IMDB ID

        Args:
            id_ (str): IMDB ID

        Returns:
            JSON: List of movies found
        """
        params = {"term": f"imdb:{id_}"}
        path = "/api/v3/movie/lookup"
        res = self.request_get(path, params=params)
        return res

    # PUT /movie/editor
    def upd_movies(self, data):
        """The Updates operation allows to edit properties of multiple movies at once

        Args:
            data (dict): Updated movie information

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "/api/v3/movie/editor"
        res = self.request_put(path, data=data)
        return res

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
        path = "/api/v3/movie/editor"
        res = self.request_del(path, data=data)
        return res

    # POST /movie/import
    def import_movies(self, data):
        """The movie import endpoint is used by the bulk import view in Radarr UI. It allows movies to be bulk added to the Radarr database.

        Args:
            data (dict): dictionary of all movies to be imported

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "/api/v3/movie/import"
        res = self.request_post(path, data=data)
        return res

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
        path = "/api/v3/moviefile"
        res = self.request_get(path, params=params)
        return res

    # GET /moviefile
    def get_movie_files(self, moviefile_ids):
        """Get movie file information for multiple movie files

        Args:
            moviefile_ids (array): an array of movie file ids

        Returns:
            JSON: List of movie files
        """
        params = {"moviefileids": moviefile_ids}
        path = "/api/v3/moviefile"
        res = self.request_get(path, params=params)
        return res

    # GET /moviefile/{id}
    def get_movie_file(self, id_):
        """Get movie file by database id

        Args:
            id_ (int): movie file id

        Returns:
            JSON: movie file information
        """
        path = f"/api/v3/moviefile/{id_}"
        res = self.request_get(path)
        return res

    # DELETE /moviefile/{id}
    def del_movie_file(self, id_):
        """Allows for deletion of a moviefile by its database id.

        Args:
            id_ (int): Movie file id

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"/api/v3/movie/{id_}"
        res = self.request_del(path)
        return res

    ## HISTORY

    # GET /history
    def get_history(
        self, page=1, page_size=20, sort_direction="descending", sort_key="date"
    ):
        """Return a json object list of items in your history

        Args:
            page (int, optional): Page to be returned. Defaults to 1.
            page_size (int, optional): Number of results per page. Defaults to 20.
            sort_direction (str, optional): Direction to sort items. Defaults to "descending".
            sort_key (str, optional): Field to sort by. Defaults to "date".

        Returns:
            JSON: Array
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortDirection": sort_direction,
            "sortKey": sort_key,
        }
        path = "/api/v3/history"
        res = self.request_get(path, params=params)
        return res

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
        path = "/api/v3/history/movie"
        res = self.request_get(path, params=params)
        return res

    ## BLACKLIST

    # GET /blacklist
    def get_blacklist(
        self,
        page=1,
        page_size=20,
        sort_direction="descending",
        sort_key="date",
    ):
        """Returns blacklisted releases.

        Args:
            page (int, optional): Page to be returned. Defaults to 1.
            page_size (int, optional): Number of results per page. Defaults to 20.
            sort_direction (str, optional): Direction to sort items. Defaults to "descending".
            sort_key (str, optional): Field to sort by. Defaults to "date".

        Returns:
            JSON: Array
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortDirection": sort_direction,
            "sortKey": sort_key,
        }
        path = "/api/v3/blacklist"
        res = self.request_get(path, params=params)
        return res

    # DELETE /blacklist
    def del_blacklist(self, id_):
        """Removes a specific release (the id provided) from the blacklist

        Args:
            id_ (int): blacklist id from database

        Returns:
            JSON: Array
        """
        params = {"id": id_}
        path = "/api/v3/blacklist"
        res = self.request_del(path, params=params)
        return res

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
        path = "/api/v3/blacklist/movie"
        res = self.request_get(path, params=params)
        return res

    # DELETE /blacklist/bulk
    def del_blacklist_bulk(self, data):
        """Delete blacklisted releases in bulk

        Args:
            data (dict): blacklists that should be deleted

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "/api/v3/blacklist/bulk"
        res = self.request_del(path, data=data)
        return res

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page=1,
        page_size=20,
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
        path = "/api/v3/queue"
        res = self.request_get(path, params=params)
        return res

    # DELETE /queue/{id}
    def del_queue(self, id_, remove_from_client=True, blacklist=True):
        """Remove an item from the queue and optionally blacklist it

        Args:
            id_ (int): id of the item to be removed
            remove_from_client (bool, optional): Remove the item from the client. Defaults to True.
            blacklist (bool, optional): Add the item to the blacklist. Defaults to True.

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        params = {"removeFromClient": remove_from_client, "blacklist": blacklist}
        path = f"/api/v3/queue/{id_}"
        res = self.request_del(path, params=params)
        return res

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
        path = "/api/v3/queue/bulk"
        res = self.request_del(path, params=params, data=data)
        return res

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
        path = "/api/v3/queue/details"
        res = self.request_get(path, params=params)
        return res

    # GET /queue/status
    def get_queue_status(self):
        """Stats on items in queue

        Returns:
            JSON: Array
        """
        path = "/api/v3/queue/status"
        res = self.request_get(path)
        return res

    # POST /queue/grab/{id}
    def force_grab_queue_item(self, id_):
        """Perform a Radarr "force grab" on a pending queue item by its ID.

        Args:
            id_ (int): queue item id from database.

        Returns:
            JSON: 200 ok, 401 Invalid API Key
        """
        path = f"/api/v3/queue/grab/{id_}"
        res = self.request_post(path)
        return res

    ## INDEXER

    # GET /indexer and /indexer/{id}
    def get_indexer(self, id_=None):
        """Get all indexers or a single indexer by its database id.

        Args:
            id_ (int, optional): indexer database id. Defaults to None.

        Returns:
            JSON: Array
        """
        if not id_:
            path = "/api/v3/indexer"
        else:
            path = f"/api/v3/indexer/{id_}"

        res = self.request_get(path)
        return res

    # PUT /indexer/{id}
    def upd_indexer(self, id_, data):
        """Edit an indexer

        Args:
            id_ (int): Database id of indexer
            data (dict): information to be changed within the indexer

        Returns:
            JSON: 200 ok, 401 Unauthorized
        """
        path = f"/api/v3/indexer/{id_}"
        res = path.request_put(path, data=data)
        return res

    # DELETE /indexer/{id}
    def del_indexer(self, id_):
        """Delete indexer by database id

        Args:
            id_ (int): DAtabase id of the indexer

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"/api/v3/indexer/{id_}"
        res = self.request_del(path)
        return res

    ## DOWNLOAD CLIENT

    # GET /downloadclient and /downloadclient/{id}
    def get_download_client(self, id_=None):
        """Get a list of all the download clients or a single client by its database id added in Radarr

        Args:
            id_ (int, optional): Download client database id. Defaults to None.

        Returns:
            JSON: Array
        """
        if not id_:
            path = "/api/v3/downloadclient"
        else:
            path = f"/api/v3/downloadclient/{id_}"

        res = self.request_get(path)
        return res

    # PUT /downloadclient/{id}
    def upd_download_client(self, id_, data):
        """Edit a downloadclient by database id

        Args:
            id_ (int): Download client database id
            data (dict): data to be updated within download client

        Returns:
            JSON: 200 Ok
        """
        path = f"/api/v3/downloadclient/{id_}"
        res = path.request_put(path, data=data)
        return res

    # DELETE /downloadclient/{id}
    def del_download_client(self, id_):
        """Delete a download client by database id

        Args:
            id_ (int): download client database id

        Returns:
            JSON: 200 Ok
        """
        path = f"/api/v3/downloadclient/{id_}"
        res = self.request_del(path)
        return res

    ## IMPORT LISTS

    # GET /importlist and /importlist/{id}
    def get_import_list(self, id_=None):
        """Query Radarr for all lists or a single list by its database id

        Args:
            id_ (int, optional): Import list database id. Defaults to None.

        Returns:
            JSON: Array
        """
        if not id_:
            path = "/api/v3/importlist"
        else:
            path = f"/api/v3/importlist/{id_}"

        res = self.request_get(path)
        return res

    # PUT /importlist/{id}
    def upd_import_list(self, id_, data):
        """Edit an importlist

        Args:
            id_ (int): Import list database id
            data (dict): data to be updated within the import list

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"/api/v3/importlist/{id_}"
        res = path.request_put(path, data=data)
        return res

    # DELETE /importlist/{id}
    def del_import_list(self, id_):
        """Delete an import list

        Args:
            id_ (int): Import list database id

        Returns:
            JSON: 200 ok, 401 Unauthorized
        """
        path = f"/api/v3/importlist/{id_}"
        res = self.request_del(path)
        return res

    ## NOTIFICATION

    # GET /notification and /notification/{id}
    def get_notification(self, id_=None):
        """Get all notifications or a single notification by its database id

        Args:
            id_ (int, optional): Notification database id. Defaults to None.

        Returns:
            JSON: Array
        """
        if not id_:
            path = "/api/v3/notification"
        else:
            path = f"/api/v3/notification/{id_}"

        res = self.request_get(path)
        return res

    # PUT /notification/{id}
    def upd_notification(self, id_, data):
        """Edit notification by database id

        Args:
            id_ (int): Database id of notification
            data (dict): data that requires updating

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"/api/v3/notification/{id_}"
        res = path.request_put(path, data=data)
        return res

    # DELETE /notification/{id}
    def del_notification(self, id_):
        """Delete a notification by its database id

        Args:
            id_ (int): Database id of notification

        Returns:
            JSON: 201 Ok, 401 Unauthorized
        """
        path = f"/api/v3/notification/{id_}"
        res = self.request_del(path)
        return res

    ## TAG

    # GET /tag and /tag/{id}
    def get_tag(self, id_=None):
        """Get all tags in the database or return a tag by database id.

        Args:
            id_ (int, optional): Database if of tag. Defaults to None.

        Returns:
            JSON: Array
        """
        if not id_:
            path = "/api/v3/tag"
        else:
            path = f"/api/v3/tag/{id_}"

        res = self.request_get(path)
        return res

    # POST /tag
    def create_tag(self, label):
        """Create a new tag that can be assigned to a movie, list, delay profile, notification, or restriction

        Args:
            label (str): Label of the tag.

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        data = {"id": 0, "label": label}
        path = "/api/v3/tag"
        res = self.request_post(path, data=data)
        return res

    # PUT /tag/{id}
    def upd_tag(self, id_, label):
        """Edit a tag by its database id

        Args:
            id_ (int): Database id of tag
            label (str): new label of the tag

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        data = {"id": id_, "label": label}
        path = f"/api/v3/tag/{id_}"
        res = self.request_put(path, data=data)
        return res

    # DELETE /tag/{id}
    def del_tag(self, id_):
        """Delete a tag

        Args:
            id_ (int): Database id of tag

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"/api/v3/tag/{id_}"
        res = self.request_del(path)
        return res

    # GET /tag/detail and /tag/detail/{id}
    def get_tag_details(self, id_=None):
        """Get a list of tag detail objects for all tags in the database,
        or the id of all items in the database which use the specified tag ID.

        Args:
            id_ (int, optional): Database id of tag. Defaults to None.

        Returns:
            JSON: Array
        """
        if not id_:
            path = "/api/v3/tag/detail"
        else:
            path = f"/api/v3/tag/detail/{id_}"

        res = self.request_get(path)
        return res

    ## DISKSPACE

    # GET /diskspace
    def get_disk_space(self):
        """Query Radarr for disk usage information
            System > Status

        Returns:
            JSON: Array
        """
        path = "/api/v3/diskspace"
        res = self.request_get(path)
        return res

    ## SETTINGS

    # GET /config/ui
    def get_config_ui(self):
        """Query Radarr for UI settings

        Returns:
            JSON: Array
        """
        path = "/api/v3/config/ui"
        res = self.request_get(path)
        return res

    # PUT /config/ui
    def upd_config_ui(self, data):
        """Edit one or many UI settings and save to to the database

        Args:
            data (dict): data to be Updated

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "/api/v3/config/ui"
        res = self.request_put(path, data=data)
        return res

    # GET /config/host
    def get_config_host(self):
        """Get General/Host settings for Radarr.

        Returns:
            JSON: Array
        """
        path = "/api/v3/config/host"
        res = self.request_get(path)
        return res

    # PUT /config/host
    def upd_config_host(self, data):
        """Edit General/Host settings for Radarr.

        Args:
            data (dict): data to bu updated

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "/api/v3/config/host"
        res = self.request_put(path, data=data)
        return res

    # GET /config/naming
    def get_config_naming(self):
        """Get Settings for movie file and folder naming.

        Returns:
            JSON: Array
        """
        path = "/api/v3/config/naming"
        res = self.request_get(path)
        return res

    # PUT /config/naming
    def upd_config_naming(self, data):
        """Edit Settings for movie file and folder naming.

        Args:
            data (dict): data to be updated

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "/api/v3/config/naming"
        res = self.request_put(path, data=data)
        return res

    ## METADATA

    # GET /metadata
    def get_metadata(self):
        """Get all metadata consumer settings

        Returns:
            JSON: Array
        """
        path = "/api/v3/metadata"
        res = self.request_get(path)
        return res

    ## SYSTEM

    # GET /system/status
    def get_system_status(self):
        """Find out information such as OS, version, paths used, etc

        Returns:
            JSON: Array
        """
        path = "/api/v3/system/status"
        res = self.request_get(path)
        return res

    ## HEALTH

    # GET /health
    def get_health(self):
        """Query radarr for health information

        Returns:
            JSON: Array
        """
        path = "/api/v3/health"
        res = self.request_get(path)
        return res

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
        path = "/api/v3/command"
        res = self.request_post(path, data=data)
        return res

    ## UPDATE

    # GET /update
    def get_updates(self):
        """Will return a list of recent updated to Radarr

        Returns:
            JSON: Array
        """
        path = "/api/v3/update"
        res = self.request_get(path)
        return res

    ## QUALITY PROFILE

    # GET /qualityProfile
    def get_quality_profiles(self):
        """Query Radarr for quality profiles

        Returns:
            JSON: Array
        """
        path = "/api/v3/qualityProfile"
        res = self.request_get(path)
        return res

    ## CALENDAR

    # GET /calendar
    def get_calendar(self, start_date, end_date, unmonitored=True):
        """Get a list of movies based on calendar Parameters

        Args:
            start_date (:obj:`datetime`): ISO 8601 start datetime
            end_date (:obj:`datetime`): ISO 8601 end datetime
            unmonitored (bool, optional): Include unmonitored movies. Defaults to True.

        Returns:
            JSON: Array
        """
        params = {
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
            "unmonitored": unmonitored,
        }
        path = "/api/v3/calendar"
        res = self.request_get(path, params=params)
        return res

    ## CUSTOM FILTERS

    # GET /customfilter
    def get_custom_filter(self):
        """Query Radarr for custom filters

        Returns:
            JSON: Array
        """
        path = "/api/v3/customfilter"
        res = self.request_get(path)
        return res

    ## REMOTE PATH MAPPING

    # GET /remotePathMapping
    def get_remote_path_mapping(self):
        """Get a list of remote paths being mapped and used by Radarr

        Returns:
            JSON: Array
        """
        path = "/api/v3/remotePathMapping"
        res = self.request_get(path)
        return res

    ## ROOT FOLDER

    # GET /rootfolder
    def get_root_folder(self):
        """Query Radarr for root folder information

        Returns:
            JSON: Array
        """
        path = "/api/v3/rootfolder"
        res = self.request_get(path)
        return res
