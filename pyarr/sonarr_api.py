from datetime import datetime

from .request_api import RequestAPI


class SonarrAPI(RequestAPI):
    """API wrapper for Sonarr endpoints."""

    def _construct_series_json(
        self,
        tvdb_id,
        quality_profile_id,
        root_dir,
        season_folder=True,
        monitored=True,
        ignore_episodes_with_files=False,
        ignore_episodes_without_files=False,
        search_for_missing_episodes=False,
    ):
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
            JSON: Array
        """
        series = self.lookup_series_by_tvdb_id(tvdb_id)[0]
        if not monitored and series.get("seasons"):
            for season in series["seasons"]:
                season["monitored"] = False

        series_json = {
            "title": series["title"],
            "seasons": series["seasons"],
            "path": root_dir + series["title"],
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
        return series_json

    ## CALENDAR

    # GET /calendar
    def get_calendar(self, start_date=None, end_date=None):
        """Gets upcoming episodes, if start/end are not supplied episodes airing today and tomorrow will be returned

        Args:
            start_date (:obj:`datetime`, optional): ISO8601 start datetime. Defaults to None.
            end_date (:obj:`datetime`, optional): ISO8601 end datetime. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "/api/calendar"
        params = {}
        if start_date:
            params["start"] = datetime.strptime(start_date, "%Y-%m-%d").strftime(
                "%Y-%m-%d"
            )
        if end_date:
            params["end"] = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")

        res = self.request_get(path, params=params)
        return res

    ## COMMAND

    # GET /command
    def get_command(self, id_=None):
        """Queries the status of a previously started command, or all currently started commands.

        Args:
            id_ (int, optional): Database id of the command. Defaults to None.

        Returns:
            JSON: Array
        """
        if id_:
            path = f"/api/command/{id_}"
        else:
            path = "/api/command"

        res = self.request_get(path)
        return res

    # POST /command
    def post_command(self, name, **kwargs):
        """Performs any of the predetermined Sonarr command routines

        Note:
            For command names and additional kwargs:
            See https://github.com/Sonarr/Sonarr/wiki/Command

        Args:
            name (str): command name that should be execured
            **kwargs: additional parameters for specific commands



        Returns:
            JSON: Array
        """
        path = "/api/command"
        data = {
            "name": name,
            **kwargs,
        }
        res = self.request_post(path, data=data)
        return res

    ## DISKSPACE

    # GET /diskspace
    def get_disk_space(self):
        """Gets information about Diskspace

        Returns:
            JSON: Array
        """
        path = "/api/diskspace"
        res = self.request_get(path)
        return res

    ## EPISODE

    # GET /episode
    def get_episodes_by_series_id(self, id_):
        """Gets all episodes from a given series ID

        Args:
            id_ (int): Database id for series

        Returns:
            JSON: Array
        """
        path = "/api/episode"
        params = {"seriesId": id_}
        res = self.request_get(path, params=params)
        return res

    # GET /episode/{id}
    def get_episode_by_episode_id(self, id_):
        """Gets a specific episode by database id

        Args:
            id_ (int): Database id for episode

        Returns:
            JSON: Array
        """
        path = f"/api/episode/{id_}"
        res = self.request_get(path)
        return res

    # PUT /episode
    def upd_episode(self, data):
        """Update the given episodes, currently only monitored is changed, all other modifications are ignored.

        Note:
            To be used in conjunction with get_episode()

        Args:
            data (dict): All parameters to update episode

        Returns:
            JSON: Array
        """
        path = "/api/episode"
        res = self.request_put(path, data=data)
        return res

    ## EPISODE FILE

    # GET /episodefile
    def get_episode_files_by_series_id(self, id_):
        """Returns all episode file information for series id specified

        Args:
            id_ (int): Database id of series

        Returns:
            JSON: Array
        """
        path = "/api/episodefile"
        params = {"seriesId": id_}
        res = self.request_get(path, params=params)
        return res

    # GET /episodefile/{id}
    def get_episode_file(self, id_):
        """Returns episode file information for specified id

        Args:
            id_ (int): Database id of episode file

        Returns:
            JSON: Array
        """
        path = f"/api/episodefile/{id_}"
        res = self.request_get(path)
        return res

    # DELETE /episodefile/{id}
    def del_episode_file(self, id_):
        """Deletes the episode file with corresponding id

        Args:
            id_ (int): Database id for episode file

        Returns:
            JSON: {}
        """
        path = f"/api/episodefile/{id_}"
        res = self.request_del(path)
        return res

    # PUT /episodefile/{id}
    def upd_episode_file_quality(self, id_, data):
        """Updates the quality of the episode file and returns the episode file

        Args:
            id_ (int): Database id for episode file
            data (dict): data with quality::

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
            JSON: Array
        """
        path = f"/api/episodefile/{id_}"
        res = self.request_put(path, data=data)
        return res

    ## HISTORY

    # GET /history
    def get_history(
        self, sort_key="date", page=1, page_size=10, sort_dir="desc", id_=None
    ):
        """Gets history (grabs/failures/completed)

        Args:
            sort_key (str, optional): series.title or date. Defaults to "date".
            page (int, optional): Page number to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_dir (str, optional): Direction to sort the items. Defaults to "desc".
            id_ (int, optional): Filter to a specific episode ID. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "/api/history"
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDir": sort_dir,
        }
        if id_:
            params["episodeId"] = id_
        res = self.request_get(path, params=params)
        return res

    ## WANTED (MISSING)

    # GET /wanted/missing
    def get_wanted(self, sort_key="airDateUtc", page=1, page_size=10, sort_dir="asc"):
        """Gets missing episode (episodes without files)

        Args:
            sort_key (str, optional): series.titke or airDateUtc. Defaults to "airDateUtc".
            page (int, optional): Page number to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_dir (str, optional): Direction to sort the items. Defaults to "asc".

        Returns:
            JSON: Array
        """
        path = "/api/wanted/missing"
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDir": sort_dir,
        }
        res = self.request_get(path, params=params)
        return res

    ## QUEUE

    # GET /queue
    def get_queue(self):
        """Gets currently downloading info

        Returns:
            JSON: Array
        """
        path = "/api/queue"
        res = self.request_get(path)
        return res

    # DELETE /queue
    def del_queue(self, id_, blacklist=False):
        """Deletes an item from the queue and download client. Optionally blacklist item after deletion.

        Args:
            id_ (int): Database id of queue item
            blacklist (bool, optional): Blacklist item after deletion. Defaults to False.

        Returns:
            JSON: {}
        """
        params = {"id": id_, "blacklist": blacklist}
        path = "/api/queue/"
        res = self.request_del(path, params=params)
        return res

    ## PARSE

    # GET /parse
    def get_parsed_title(self, title):
        """Returns the result of parsing a title. series and episodes will be
        returned only if the parsing matches to a specific series and one or more
        episodes. series and episodes will be formatted the same as Series and Episode
        responses.

        Args:
            title (string): Title of series / episode

        Returns:
            JSON: Array
        """
        params = {"title": title}
        path = "/api/parse"
        res = self.request_get(path, params=params)
        return res

    # GET /parse
    def get_parsed_path(self, file_path):
        """Returns the result of parsing a file path. series and episodes will be
        returned only if the parsing matches to a specific series and one or more
        episodes. series and episodes will be formatted the same as Series and Episode
        responses.

        Args:
            file_path (string): file path of series / episode

        Returns:
            JSON: Array
        """
        params = {"path": file_path}
        path = "/api/parse"
        res = self.request_get(path, params=params)
        return res

    ## PROFILE

    # GET /profile
    def get_quality_profiles(self):
        """Gets all quality profiles

        Returns:
            JSON: Array
        """
        path = "/api/profile"
        res = self.request_get(path)
        return res

    ## RELEASE

    # GET /release
    def get_releases(self, id_):
        """Get a release with a specific episode ID.

        Args:
            id_ (int): Database id for episode

        Returns:
            JSON: Array
        """
        params = {"episodeId": id_}
        path = "/api/release"
        res = self.request_get(path, params=params)
        return res

    # POST /release
    def download_release(self, guid, indexer_id):
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
        path = "/api/release"
        res = self.request_post(path, data=data)
        return res

    # POST /release/push
    def push_release(self, title, download_url, protocol, publish_date):
        """If the title is wanted, Sonarr will grab it.

        Args:
            title (str): Release name
            download_url (str): .torrent file URL
            protocol (str): "Usenet" or "Torrent
            publish_date (str): ISO8601 date string

        Returns:
            JSON: Array
        """
        data = {
            "title": title,
            "downloadUrl": download_url,
            "protocol": protocol,
            "publishDate": publish_date,
        }
        path = "/api/release/push"
        res = self.request_post(path, data=data)
        return res

    ## ROOT FOLDER

    # GET /rootfolder
    def get_root_folder(self):
        """Gets root folder

        Returns:
            JSON: Array
        """
        path = "/api/rootfolder"
        res = self.request_get(path)
        return res

    ## SERIES
    # GET /series and /series/{id}
    def get_series(self, id_=None):
        """Returns all series in your collection or the series with the matching
        series ID if one is found.

        Args:
            id_ (int, optional): Database id for series. Defaults to None.

        Returns:
            JSON: Array
        """
        if id_:
            path = f"/api/series/{id_}"
        else:
            path = "/api/series"

        res = self.request_get(path)
        return res

    # POST /series
    def add_series(
        self,
        tvdb_id,
        quality_profile_id,
        root_dir,
        season_folder=True,
        monitored=True,
        ignore_episodes_with_files=False,
        ignore_episodes_without_files=False,
        search_for_missing_episodes=False,
    ):
        """Adds a new series to your collection

        Note:
            if you do not add the required params, then the series wont function. some of these without the others can
            indeed make a "series". But it wont function properly in nzbdrone.

        Args:
            tvdb_id (int): TDDB Id
            quality_profile_id (int): Database id for quality profile
            root_dir (str): Root folder location, full path will be created from this
            season_folder (bool, optional): Create a folder for each season. Defaults to True.
            monitored (bool, optional): Monitor this series. Defaults to True.
            ignore_episodes_with_files (bool, optional): Ignore any episodes with existing files. Defaults to False.
            ignore_episodes_without_files (bool, optional): Ignore any episodes without existing files. Defaults to False.
            search_for_missing_episodes (bool, optional): Search for missing episodes to download. Defaults to False.

        Returns:
            JSON: Array
        """
        series_json = self._construct_series_json(
            tvdb_id,
            quality_profile_id,
            root_dir,
            season_folder,
            monitored,
            ignore_episodes_with_files,
            ignore_episodes_without_files,
            search_for_missing_episodes,
        )

        path = "/api/series"
        res = self.request_post(path, data=series_json)
        return res

    # PUT /series
    def upd_series(self, data):
        """Update an existing series

        Args:
            data (dict): contains data obtained by get_series()

        Returns:
            JSON: Array
        """
        path = "/api/series"
        res = self.request_put(path, data=data)
        return res

    # DELETE /series/{id}
    def del_series(self, id_, delete_files=False):
        """Delete the series with the given id

        Args:
            id_ (int): Database id for series
            delete_files (bool, optional): If true series folder and files will be deleted. Defaults to False.

        Returns:
            JSON: {}
        """
        # File deletion does not work
        params = {"deleteFiles": delete_files}
        path = f"/api/series/{id_}"
        res = self.request_del(path, params=params)
        return res

    # GET /series/lookup
    def lookup_series(self, term):
        """Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

        Args:
            term (str): Series' Name, using `%20` to signify spaces, as in `The%20Blacklist`

        Returns:
            JSON: Array
        """
        params = {"term": term}
        path = "/api/series/lookup"
        res = self.request_get(path, params=params)
        return res

    # GET /series/lookup
    def lookup_series_by_tvdb_id(self, id_):
        """Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

        Args:
            id_ (int): TVDB ID

        Returns:
            JSON: Array
        """
        params = {"term": f"tvdb:{id_}"}
        path = "/api/series/lookup"
        res = self.request_get(path, params=params)
        return res

    ## SYSTEM

    # GET /system/status
    def get_system_status(self):
        """Returns system status

        Returns:
            JSON: Array
        """
        path = "/api/system/status"
        res = self.request_get(path)
        return res

    # GET /system/backup
    def get_backup(self):
        """Returns the list of available backups

        Returns:
            JSON: Array
        """
        path = "/api/system/backup"
        res = self.request_get(path)
        return res

    ## TAG

    # GET /tag and /tag/{id}
    def get_tag(self, id_=None):
        """Returns all tags or specific tag by database id

        Args:
            id_ (int, optional): Database id for tag. Defaults to None.

        Returns:
            JSON: Array
        """
        if not id_:
            path = "/api/tag"
        else:
            path = f"/api/tag/{id_}"

        res = self.request_get(path)
        return res

    # POST /tag
    def create_tag(self, label):
        """Adds a new tag

        Args:
            label (str): Tag name / label

        Returns:
            JSON: Array
        """
        data = {"label": label}
        path = "/api/tag"
        res = self.request_post(path, data=data)
        return res

    # PUT /tag/{id}
    def upd_tag(self, id_, label):
        """Update an existing tag

        Note:
            You should perform a get_tag() and submit the full body with changes

        Args:
            id_ (int): Database id of tag
            label (str): tag name / label

        Returns:
            JSON: Array
        """
        data = {"id": id_, "label": label}
        path = f"/api/tag/{id_}"
        res = self.request_put(path, data=data)
        return res

    # DELETE /tag/{id}
    def del_tag(self, id_):
        """Delete the tag with the given ID

        Args:
            id_ (int): Database id of tag

        Returns:
            JSON: {}
        """
        path = f"/api/tag/{id_}"
        res = self.request_del(path)
        return res

    ## LOG

    # GET /log
    def get_logs(
        self,
        page=1,
        page_size=10,
        sort_key="time",
        sort_dir="desc",
        filter_key=None,
        filter_value="All",
    ):
        """Gets sonarr logs

        Args:
            page (int, optional): Specifiy page to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_key (str, optional): Field to sort by. Defaults to "time".
            sort_dir (str, optional): Direction to sort. Defaults to "desc".
            filter_key (str, optional): Key to filter by. Defaults to None.
            filter_value (str, optional): Value of the filter. Defaults to "All".

        Returns:
            JSON: Array
        """
        path = "/api/log"
        params = {
            "page": page,
            "pageSize": page_size,
            "sortKey": sort_key,
            "sortDir": sort_dir,
            "filterKey": filter_key,
            "filterValue": filter_value,
        }
        res = self.request_get(path, params=params)
        return res
