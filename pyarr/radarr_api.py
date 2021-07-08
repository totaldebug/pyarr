# -*- coding: utf-8 -*-
from .request_api import RequestAPI


class RadarrAPI(RequestAPI):
    """API wrapper for Radarr endpoints."""

    def construct_movie_json(
        self, db_id, quality_profile_id, root_dir, monitored=True, search_for_movie=True
    ):
        """Searches for movie on tmdb and returns Movie json to add.

        Args:
            [Required] db_id (str): imdb or tmdb id
            [Required] quality_profile_id (int)
            [Required] root_dir (str)
            [Optional] monitored (bool)
            [Optional] search_for_movie (bool)

        Return:
            Movie JSON (dict)
        """
        s_dict = self.lookup_movie(db_id)

        if not s_dict:
            raise Exception("Movie Doesn't Exist")

        movie_json = {
            "title": s_dict[0]["title"],
            "rootFolderPath": root_dir,
            "qualityProfileId": quality_profile_id,
            "year": s_dict[0]["year"],
            "tmdbId": s_dict[0]["tmdbId"],
            "images": s_dict[0]["images"],
            "titleSlug": s_dict[0]["titleSlug"],
            "monitored": monitored,
            "addOptions": {"searchForMovie": search_for_movie},
        }
        return movie_json

    ## MOVIE

    # GET /movie
    def get_movie(self, **kwargs):
        """Returns all movies in the database, or returns a movie with a specific TMDB ID.

        Args:
            [Optional] tmdbId (int)
        Returns:
            json response
        """
        path = "/api/v3/movie"
        res = self.request_get(path, params=kwargs)
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
        """addMovie adds a new movie to collection

        Args:
            [Required] db_id (str)
            [Required] quality_profile_id (int)
            [Required] root_dir (str)
            [Optional] monitored (bool)
            [Optional] search_for_movie (bool)
            [Optional] tmdb (bool): Set to false to use imdb IDs
        Returns:
            json response
        """
        if tmdb:
            term = f"tmdb:{str(db_id)}"
        else:
            term = f"imdb:{str(db_id)}"

        movie_json = self.construct_movie_json(
            term, quality_profile_id, root_dir, monitored, search_for_movie
        )

        path = "/api/v3/movie"
        res = self.request_post(path, data=movie_json)
        return res

    # PUT /movie
    def update_movie(self, data, move_files=False):
        """Update an existing movie.

        Args:
            [Required] data (dict): Dictionary containing an object obtained by get_movie()
        Kwargs:
            [Optional] move_files (bool): Have radarr move files when updating
        Returns:
            json response
        """

        path = "/api/movie"
        params = {"moveFiles": move_files}
        res = self.request_put(path, data=data, params=params)
        return res

    # GET /movie/{id}
    def get_movie_by_id(self, id_):
        """Get a movie by the database ID.

        Args:
            [Optional] id_ (int)
        Returns:
            json response
        """
        path = f"/api/v3/movie/{id_}"
        res = self.request_get(path)
        return res

    # DELETE /movie/{id}
    def del_movie(self, id_, del_files=False, add_exclusion=False):
        """Delete a single movie by database ID.
        Args:
            [Required] id_ (int)
            [Optional] del_files (bool)
            [Optional] add_exclusion (bool)
        Returns:
            json response
        """
        params = {"deleteFiles": del_files, "addExclusion": add_exclusion}
        path = f"/api/v3/movie/{id_}"
        res = self.request_del(path, params=params)
        return res

    # GET /movie/lookup
    def lookup_movie(self, term):
        """Searches for movie.

        Args:
            [Required] term (str): Uses TMDB for search results
        Returns:
            json response
        """
        params = {"term": term}
        path = "/api/v3/movie/lookup"
        res = self.request_get(path, params=params)
        return res

    # GET /movie/lookup
    def lookup_movie_by_tmdb_id(self, id_):
        """Searches for movie.

        Args:
            [Required] term (str): Uses TMDB for search results
        Returns:
            json response
        """
        params = {"term": f"tmdb:{id_}"}
        path = "/api/v3/movie/lookup"
        res = self.request_get(path, params=params)
        return res

    # PUT /movie/editor
    def update_movies(self, data):
        """Edit multiple movie files.

        Args:
            [Required] data (dict)
        Returns:
            json response
        """
        path = "/api/v3/movie/editor"
        res = self.request_put(path, data=data)
        return res

    # DELETE /movie/editor
    def del_movies(self, data):
        """Delete multiple movie files.

        Args:
            [Required] data (dict)
        Returns:
            json response
        """
        path = "/api/v3/movie/editor"
        res = self.request_del(path, data=data)
        return res

    # POST /movie/import
    def import_movies(self, data):
        """Import mulitple movies.

        Args:
            [Required] data (dict)
        Returns:
            json response
        """
        path = "/api/v3/movie/import"
        res = self.request_post(path, data=data)
        return res

    ## MOVIEFILE

    # GET /moviefile
    def get_movie_files_by_movie_id(self, id_):
        """Returns the movie files belonging to a specific movie based on database ID.

        Args:
            [Required] id_ (int)
        Returns:
            json response
        """
        params = {"movieid": id_}
        path = "/api/v3/moviefile"
        res = self.request_get(path, params=params)
        return res

    # GET /moviefile
    def get_movie_files(self, moviefile_ids):
        """Returns movie file info for multiple movie files.

        Args:
            [Required] moviefile_ids (array:int)
        Returns:
            json response
        """
        params = {"moviefileids": moviefile_ids}
        path = "/api/v3/moviefile"
        res = self.request_get(path, params=params)
        return res

    # GET /moviefile/{id}
    def get_movie_file(self, id_):
        """Returns movie file info.

        Args:
            [Required] id_ (int)
        Returns:
            json response
        """
        path = f"/api/v3/moviefile/{id_}"
        res = self.request_get(path)
        return res

    # DELETE /moviefile/{id}
    def del_movie_file(self, id_):
        """Allows for deletion of a moviefile by its database ID.
        Args:
            [Required] id_ (int)
        Returns:
            json response
        """
        path = f"/api/v3/movie/{id_}"
        res = self.request_del(path)
        return res

    ## HISTORY

    # GET /history
    def get_history(
        self, page, page_size=20, sort_direction="descending", sort_key="date"
    ):
        """Return a json object list of items in your history

        Args:
            [Required] page (int)
            [Optional] page_size (int): Default: 20
            [Optional] sort_direction (str): Default: descending
            [Optional] sort_key (str): Default: date
        Returns:
            json response
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
        """Return a json object list of items in your history.

        Args:
            [Required] id_ (int): Database ID of movie
            [Optional] event_type (int): History event type to retrieve
        Returns:
            json response
        """
        params = {"movieId": id_}
        if event_type:
            params["eventType"] = event_type
        path = "/api/v3/history/movie"
        res = self.request_get(path, params=params)
        return res

    ## BLACKLIST

    # TODO: GET /blacklist
    # TODO: DELETE /blacklist
    # TODO: GET /blacklist/movie
    # TODO: DELETE /blacklist/bulk

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page,
        page_size=20,
        sort_direction="ascending",
        sort_key="timeLeft",
        include_unknown_movie_items=True,
    ):
        """Return a json object list of items in the queue.
        Args:
            [Required] page (int)
            [Optional] page_size (int): Default: 20
            [Optional] sort_direction (str): Default: ascending
            [Optional] sort_key (str): Default: timeLeft
            [Optional] include_unknown_movie_items (bool): Default: True
        Returns:
            json response
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

    # TODO: DELETE /queue/{id}
    # TODO: DELETE /queue/bulk
    # TODO: GET /queue/details
    # TODO: GET /queue/status
    # TODO: POST /queue/grab/{id}

    ## INDEXER

    # GET /indexer and /indexer/{id}
    def get_indexer(self, id_=None):
        """Get all indexers or a single indexer by its database ID.

        Args:
            [Optional] id_ (int)
        Returns:
            json response
        """
        if not id_:
            path = "/api/v3/indexer"
        else:
            path = f"/api/v3/indexer/{id_}"

        res = self.request_get(path)
        return res

    # PUT /indexer/{id}
    def update_indexer(self, id_, data):
        """Edit an indexer.

        Args:
            [Required] id_ (int)
            [Required] data (dict)
        Returns:
            json response
        """
        path = f"/api/v3/indexer/{id_}"
        res = path.request_put(path, data=data)
        return res

    # DELETE /indexer/{id}
    def del_indexer(self, id_):
        """Delete and indexer.

        Args:
            [Required] id_ (int)
        Returns:
            json response
        """
        path = f"/api/v3/indexer/{id_}"
        res = self.request_del(path)
        return res

    ## DOWNLOAD CLIENT

    # GET /downloadclient and /downloadclient/{id}
    def get_downloadclient(self, id_=None):
        """Get all download clients or a single download client by its database ID.

        Args:
            [Optional] id_ (int)
        Returns:
            json response
        """
        if not id_:
            path = "/api/v3/downloadclient"
        else:
            path = f"/api/v3/downloadclient/{id_}"

        res = self.request_get(path)
        return res

    # PUT /downloadclient/{id}
    def update_downloadclient(self, id_, data):
        """Edit an downloadclient.

        Args:
            [Required] id_ (int)
            [Required] data (dict)
        Returns:
            json response
        """
        path = f"/api/v3/downloadclient/{id_}"
        res = path.request_put(path, data=data)
        return res

    # DELETE /downloadclient/{id}
    def del_downloadclient(self, id_):
        """Delete an downloadclient.

        Args:
            [Required] id_ (int)
        Returns:
            json response
        """
        path = f"/api/v3/downloadclient/{id_}"
        res = self.request_del(path)
        return res

    ## IMPORT LISTS

    # GET /importlist and /importlist/{id}
    def get_importlist(self, id_=None):
        """Get all import lists or a single import list by its database ID.

        Args:
            [Optional] id_ (int)
        Returns:
            json response
        """
        if not id_:
            path = "/api/v3/importlist"
        else:
            path = f"/api/v3/importlist/{id_}"

        res = self.request_get(path)
        return res

    # PUT /importlist/{id}
    def update_importlist(self, id_, data):
        """Edit an importlist.

        Args:
            [Required] id_ (int)
            [Required] data (dict)
        Returns:
            json response
        """
        path = f"/api/v3/importlist/{id_}"
        res = path.request_put(path, data=data)
        return res

    # DELETE /importlist/{id}
    def del_importlist(self, id_):
        """Delete an importlist.

        Args:
            [Required] id_ (int)
        Returns:
            json response
        """
        path = f"/api/v3/importlist/{id_}"
        res = self.request_del(path)
        return res

    ## NOTIFICATION

    # GET /notification and /notification/{id}
    def get_notification(self, id_=None):
        """Get all notifications or a single notification by its database ID.

        Args:
            [Optional] id_ (int)
        Returns:
            json response
        """
        if not id_:
            path = "/api/v3/notification"
        else:
            path = f"/api/v3/notification/{id_}"

        res = self.request_get(path)
        return res

    # PUT /notification/{id}
    def update_notification(self, id_, data):
        """Edit a notification.

        Args:
            [Required] id_ (int)
            [Required] data (dict)
        Returns:
            json response
        """
        path = f"/api/v3/notification/{id_}"
        res = path.request_put(path, data=data)
        return res

    # DELETE /notification/{id}
    def del_notification(self, id_):
        """Delete a notification.

        Args:
            [Required] id_ (int)
        Returns:
            json response
        """
        path = f"/api/v3/notification/{id_}"
        res = self.request_del(path)
        return res

    ## TAG

    # TODO: GET /tag
    # TODO: POST /tag
    # TODO: GET /tag/detail
    # TODO: GET /tag/detail/{id}
    # TODO: GET /tag/{id}
    # TODO: DELETE /tag/{id}
    # TODO: PUT /tag/{id}

    ## DISKSPACE

    # GET /diskspace
    def get_disk_space(self):
        """Query Radarr for disk usage information.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/diskspace"
        res = self.request_get(path)
        return res

    ## SETTINGS

    # GET /config/ui
    def get_config_ui(self):
        """Query Radarr for UI settings

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/config/ui"
        res = self.request_get(path)
        return res

    # PUT /config/ui
    def update_config_ui(self, data):
        """Edit one or many UI Settings and save to the database.

        Args:
            [Required] data (dict)
        Returns:
            json response
        """
        path = "/api/v3/config/ui"
        res = self.request_put(path, data=data)
        return res

    # GET /config/host
    def get_config_host(self):
        """Get General/Host settings for Radarr.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/config/host"
        res = self.request_get(path)
        return res

    # PUT /config/host
    def update_config_host(self, data):
        """Edit General/Host settings for Radarr.

        Args:
            [Required] data (dict)
        Returns:
            json response
        """
        path = "/api/v3/config/host"
        res = self.request_put(path, data=data)
        return res

    # GET /config/naming
    def get_config_naming(self):
        """Get Settings for movie file and folder naming.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/config/naming"
        res = self.request_get(path)
        return res

    # PUT /config/naming
    def update_config_naming(self, data):
        """Edit Settings for movie file and folder naming.

        Args:
            [Required] data (dict)
        Returns:
            json response
        """
        path = "/api/v3/config/naming"
        res = self.request_put(path, data=data)
        return res

    ## METADATA

    # GET /metadata
    def get_metadata(self):
        """Get all metadata consumer settings.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/metadata"
        res = self.request_get(path)
        return res

    ## SYSTEM

    # GET /system/status
    def get_system_status(self):
        """Find out information such as OS, version, paths used, etc.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/system/status"
        res = self.request_get(path)
        return res

    ## HEALTH

    # GET /health
    def get_health(self):
        """Query radarr for health information.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/health"
        res = self.request_get(path)
        return res

    ## COMMAND

    # POST /command
    def post_command(self, name, value=None):
        """Performs any of the predetermined Radarr command routines.

        Kwargs:
            [Required] name (str).
            [Optional] value (str): If the command requires a value, specify it here.

            Options available:
                - ApplicationUpdate - Trigger an update of Radarr
                - Backup - Trigger a backup routine
                - CheckHealth - Trigger a system health check
                - ClearBlacklist - Triggers the removal of all blacklisted movies
                - CleanUpRecycleBin - Trigger a recycle bin cleanup check
                - DeleteLogFiles - Triggers the removal of all Info/Debug/Trace log files
                - DeleteUpdateLogFiles - Triggers the removal of all Update log files
                - DownloadedMoviesScan - Triggers the scan of downloaded movies
                - MissingMoviesSearch - Triggers a search of all missing movies
                - RefreshMonitoredDownloads - Triggers the scan of monitored downloads
                - RefreshMovie - Trigger a refresh / scan of library
                    - movieIds:int[] - a list of ids (comma separated) for movies to refresh

            See https://radarr.video/docs/api/#/Command/post-command
        Returns:
        json response

        """
        path = "/api/v3/command"
        data = {name: value}
        res = self.request_post(path, data=data)
        return res

    ## UPDATE

    # GET /update
    def get_update(self):
        """Returns a list of recent updates to Radarr.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/update"
        res = self.request_get(path)
        return res

    ## QUALITY PROFILE

    # GET /qualityProfile
    def get_quality_profiles(self):
        """Query Radarr for quality profiles.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/qualityProfile"
        res = self.request_get(path)
        return res

    ## CALENDAR

    # GET /calendar
    def get_calendar(self, start_date, end_date, unmonitored=True):
        """Get a list of movies based on calendar parameters.

        Args:
            [Required]
                - start_date (datetime): ISO 8601
                - end_date (datetime): ISO 8601
            [Optional] unmonitored (bool)

        Returns:
            json response
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
        """Query Radarr for custom filters.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/customfilter"
        res = self.request_get(path)
        return res

    ## REMOTE PATH MAPPING

    # GET /remotePathMapping
    def get_remote_path_mapping(self):
        """Get a list of remote paths being mapped and used by Radarr.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/remotePathMapping"
        res = self.request_get(path)
        return res

    ## ROOT FOLDER

    # GET /rootfolder
    def get_root(self):
        """Returns the Root Folder.

        Args:
            None
        Returns:
            json response
        """
        path = "/api/v3/rootfolder"
        res = self.request_get(path)
        return res
