from datetime import datetime

from .request_api import RequestAPI


class SonarrAPI(RequestAPI):
    """API wrapper for Sonarr endpoints."""

    def construct_series_json(
        self,
        tvdbId,
        qualityProfileId,
        rootDir,
        seasonFolder=True,
        monitored=True,
        ignoreEpisodesWithFiles=False,
        ignoreEpisodesWithoutFiles=False,
        searchForMissingEpisodes=False,
    ):
        """Searches for new shows on trakt and returns Series json to add

        Args:
            [Required] tvdbID (int)
            [Required] qualityProfileId (int)
            [Required] rootDir (str)
            [Optional] seasonFolder (bool)
            [Optional] monitored (bool)
            [Optional] ignoreEpisodesWithFiles (bool)
            [Optional] ignoreEpisodesWithoutFiles (bool)
            [Optional] searchForMissingEpisodes (bool)
        Returns:
            JSON Response
        """
        res = self.lookup_series(tvdbId)
        s_dict = res[0]
        if not monitored:
            for season in s_dict["seasons"]:
                season["monitored"] = False

        series_json = {
            "title": s_dict["title"],
            "seasons": s_dict["seasons"],
            "path": rootDir + s_dict["title"],
            "qualityProfileId": qualityProfileId,
            "seasonFolder": seasonFolder,
            "monitored": monitored,
            "tvdbId": tvdbId,
            "images": s_dict["images"],
            "titleSlug": s_dict["titleSlug"],
            "addOptions": {
                "ignoreEpisodesWithFiles": ignoreEpisodesWithFiles,
                "ignoreEpisodesWithoutFiles": ignoreEpisodesWithoutFiles,
                "searchForMissingEpisodes": searchForMissingEpisodes,
            },
        }
        return series_json

    ## CALENDAR

    # GET /calendar
    def get_calendar(self, *args):
        """Retrieves info about when series were/will be downloaded.
        If no start and end, retrieves series airing today and tomorrow.

        Args:
            start_date:
            end_date:
        Returns:
            JSON Response
        """
        path = "/api/calendar"
        data = {}
        if args:
            start_date = args[0]
            end_date = args[1]

            startDate = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            data.update({"start": startDate})

            endDate = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            data.update({"end": endDate})

        res = self.request_get(path, **data)
        return res

    ## COMMAND

    # GET /command
    def get_command(self, *args):
        """Queries the status of a previously
        started command, or all currently started commands.

        Args:
            [Optional] id (int) Unique ID of command
        Returns:
            JSON Response
        """
        if len(args) == 1:
            path = f"/api/command/{args[0]}"
        else:
            path = "/api/command"

        res = self.request_get(path)
        return res

    # POST /command
    def set_command(self, **kwargs):
        """Performs any of the predetermined Sonarr command routines.

        Kwargs:
            [Required] name (str).

            Options available: RefreshSeries, RescanSeries, EpisodeSearch,
                SeasonSearch, SeriesSearch, DownloadedEpisodesScan, RssSync,
                RenameFiles, RenameSeries, Backup, missingEpisodeSearch

            Additional Parameters may be required or optional...
            See https://github.com/Sonarr/Sonarr/wiki/Command
        Returns:
            JSON Response
        """
        path = "/api/command"

        data = kwargs
        res = self.request_post(path, data=data)
        return res

    ## DISKSPACE

    # GET /diskspace
    def get_disk_space(self):
        """Retrieves info about the disk space on the server.

        Args:
            None
        Returns:
            JSON Response
        """
        path = "/api/diskspace"
        res = self.request_get(path)
        return res

    ## EPISODE

    # GET /episode
    def get_episodes_by_series_id(self, seriesId):
        """Returns all episodes for the given series

        Args:
            seriesId (int):
        Returns:
            JSON Response
        """
        path = f"/api/episode?seriesId={seriesId}"
        res = self.request_get(path)
        return res

    # GET /episode/{id}
    def get_episode_by_episode_id(self, episodeId):
        """Returns the episode with the matching id

        Args:
            episode_id (int):
        Returns:
            JSON Response
        """
        path = f"/api/episode/{episodeId}"
        res = self.request_get(path)
        return res

    # PUT /episode
    def upd_episode(self, data):
        """Update the given episodes, currently only monitored is changed, all
        other modifications are ignored. All parameters (you should perform a
        GET/{id} and submit the full body with the changes, as other values may
        be editable in the future.

        Args:
            data (dict) - data payload
        Returns:
            JSON Response
        """
        path = "/api/episode"
        res = self.request_put(path, data=data)
        return res

    ## EPISODE FILE

    # GET /episodefile
    def get_episode_files_by_series_id(self, id_):
        """Returns all episode files for the given series.

        Args:
            [Required] id_ (int):
        Returns:
            JSON Response
        """
        params = {"seriesId": id_}
        path = "/api/episodefile"
        res = self.request_get(path, params=params)
        return res

    # GET /episodefile/{id}
    def get_episode_file(self, id_):
        """Returns the episode file with the matching ID.

        Kwargs:
            [Required] id_ (int)
        Returns:
            JSON Response
        """
        path = f"/api/episodefile/{id_}"
        res = self.request_get(path)
        return res

    # DELETE /episodefile/{id}
    def del_episode_file(self, id_):
        """Delete the given episode file.

        Kwargs:
            [Required] id_ (str)
        Returns:
            JSON Response
        """
        path = f"/api/episodefile/{id_}"
        res = self.request_del(path)
        return res

    # PUT /episodefile/{id}
    def upd_episode_file_quality(self, id_, data):
        """Updates the quality of the episode file and returns the episode file.

        Kwargs:
            [Required] id_ (str)
            [Required] data (dict) - See Sonarr docs for formatting

        Returns:
            JSON Response
        """
        path = f"/api/episodefile/{id_}"
        res = self.request_put(path, data=data)
        return res

    ## HISTORY

    # GET /history
    def get_history(self, **kwargs):
        """Gets history (grabs/failures/completed)

        Args:
            [Required] sortKey (str) - series.title or date (default)
            [Optional] page (int) - 1-indexed
            [Optional] pageSize (int) - Default: 0
            [Optional] sortDir (str) - asc or desc - Default: asc
            [Optional] episodeId (int) - Filters to a specific episode ID
        Returns:
            JSON Response
        """
        data = {}
        data.update({"sortKey": kwargs.get("sortKey", "date")})
        for key, value in kwargs.items():
            data.update({key: value})
        path = "/api/history"
        res = self.request_get(path, **data)
        return res

    ## WANTED (MISSING)

    # GET /wanted/missing
    def get_wanted(self, **kwargs):
        """Gets Wanted / Missing episodes

        Args:
            [Required] sortKey (str) - series.title or airDateUtc (default)
            [Optional] page (int) - 1-indexed Default: 1
            [Optional] pageSize (int) - Default: 10
            [Optional] sortDir (str) - asc or desc - Default: asc
        Returns:
            JSON Response
        """
        data = {}
        data.update({"sortKey": kwargs.get("sortKey", "airDateUtc")})
        for key, value in kwargs.items():
            data.update({key: value})
        path = "/api/wanted/missing"
        res = self.request_get(path, **data)
        return res

    ## QUEUE

    # GET /queue
    def get_queue(self):
        """Gets current downloading info

        Args:
            None
        Returns:
            JSON Response
        """
        path = "/api/queue"
        res = self.request_get(path)
        return res

    # DELETE /queue
    def del_queue(self, id_, blacklist=True):
        """Deletes an item from the queue and download client.
        Optionally blacklist item after deletion.

        Args:
            [Required] id_ (int)
            [Optional] blacklist (bool) - Default: True
        Returns:
            JSON Response
        """
        params = {"id": id_, "blacklist": blacklist}
        path = "/api/queue/"
        res = self.request_del(path, params=params)
        return res

    ## PARSE

    # GET /parse
    def get_parsed_title(self, title):
        """Returns the result of parsing a title.

        Args:
            title (str)
        Returns:
            JSON Response
        """
        params = {"title": title}
        path = "/api/parse"
        res = self.request_get(path, params=params)
        return res

    # GET /parse
    def get_parsed_path(self, path):
        """Returns the result of parsing a path.

        Args:
            path (str)
        Returns:
            JSON Response
        """
        params = {"path": path}
        path_ = "/api/parse"
        res = self.request_get(path_, params=params)
        return res

    ## PROFILE

    # GET /profile
    def get_quality_profiles(self):
        """Gets all quality profiles

        Args:
            None
        Returns:
            JSON Response
        """
        path = "/api/profile"
        res = self.request_get(path)
        return res

    ## RELEASE

    # TODO: GET /release

    # TODO: POST /reease

    # POST /release/push
    def push_release(self, title, download_url, protocol, publish_date):
        """Notifies Sonarr of a new release.
        title: release name
        downloadUrl: .torrent file URL
        protocol: usenet / torrent
        publishDate: ISO8601 date string

        Args:
            [Required] title (str)
            [Required] download_url (str)
            [Required] protocol (str) - "Usenet" or "Torrent"
            [Required] publish_date (str)
        Returns:
            JSON Response
        """
        params = {
            "title": title,
            "downloadUrl": download_url,
            "protocol": protocol,
            "publishDate": publish_date,
        }
        path = "/api/release/push"
        res = self.request_post(path, params=params)
        return res

    ## ROOT FOLDER

    # GET /rootfolder
    def get_root_folder(self):
        """Returns the Root Folder

        Args:
            None
        Returns:
            JSON Response
        """
        path = "/api/rootfolder"
        res = self.request_get(path)
        return res

    ## SERIES
    # GET /series and /series/{id}
    def get_series(self, *args):
        """Return all series in your collection or
        the series with the matching ID if one is found

        Args:
            [Optional] seriesID
        Returns:
            JSON Response
        """
        if len(args) == 1:
            path = f"/api/series/{args[0]}"
        else:
            path = "/api/series"

        res = self.request_get(path)
        return res

    # POST /series
    def add_series(
        self,
        tvdbId,
        qualityProfileId,
        rootDir,
        seasonFolder=True,
        monitored=True,
        ignoreEpisodesWithFiles=False,
        ignoreEpisodesWithoutFiles=False,
        searchForMissingEpisodes=False,
    ):
        """Add a new series to your collection

        Args:
            [Required] tvdbID (int)
            [Required] qualityProfileId (int)
            [Required] rootDir (str)
            [Optional] seasonFolder (bool)
            [Optional] monitored (bool)
            [Optional] ignoreEpisodesWithFiles (bool)
            [Optional] ignoreEpisodesWithoutFiles (bool)
            [Optional] searchForMissingEpisodes (bool)
        Returns:
            JSON Response
        """
        series_json = self.construct_series_json(
            tvdbId,
            qualityProfileId,
            rootDir,
            seasonFolder,
            monitored,
            ignoreEpisodesWithFiles,
            ignoreEpisodesWithoutFiles,
            searchForMissingEpisodes,
        )

        path = "/api/series"
        res = self.request_post(path, data=series_json)
        return res

    # PUT /series
    def upd_series(self, data):
        """Update an existing series.

        Args:
            data (dictionary containing an object obtained by getSeries())
        Returns:
            JSON Response
        """
        path = "/api/series"
        res = self.request_put(path, data=data)
        return res

    # DELETE /series/{id}
    def del_series(self, seriesId, delFiles=False):
        """Delete the series with the given ID

        Args:
            seriesId (int)
            delFiles (bool)
        Returns:
            JSON Response
        """
        # File deletion does not work
        data = {"deleteFiles": delFiles}
        path = f"/api/series/{seriesId}"
        res = self.request_del(path, data=data)
        return res

    # GET /series/lookup
    def lookup_series(self, term):
        """Searches for new shows on tvdb

        Args:
            [Required] term (str)
        Returns:
            JSON Response
        """
        params = {"term": term}
        path = "/api/series/lookup"
        res = self.request_get(path, params=params)
        return res

    # GET /series/lookup
    def lookup_series_by_tvdb_id(self, id_):
        """Searches for new shows on tvdb

        Args:
            [Required] id_ (int) - TVDB ID of a show
        Returns:
            JSON Response
        """
        params = {"term": f"tvdb:{id_}"}
        path = "/api/series/lookup"
        res = self.request_get(path, params=params)
        return res

    ## SYSTEM

    # GET /system/status
    def get_system_status(self):
        """Returns the System Status as json

        Args:
            None
        Returns:
            JSON Response
        """
        path = "/api/system/status"
        res = self.request_get(path)
        return res

    # GET /system/backup
    def get_backup(self):
        """Returns the backups as json

        Args:
            None
        Returns:
            JSON Response
        """
        path = "/api/system/backup"
        res = self.request_get(path)
        return res

    ## TAGS

    # TODO: GET /tag and /tag/{id}

    # TODO: POST /tag

    # TODO: PUT /tag

    # TODO: DELETE /tag/{id}

    ## LOG

    # GET /log
    def get_logs(self, **kwargs):
        """Gets Sonarr Logs

        Kwargs:
            [Required] None
            [Optional] page (int) - Page number - Default: 1.
            [Optional] pageSize (int) - Records per page - Default: 10.
            [Optional] sortKey (str) - What key to sort on - Default: 'time'.
            [Optional] sortDir (str) - asc or desc - Default: desc.
            [Optional] filterKey (str) - What key to filter - Default: None.
            [Optional] filterValue (str) - Warn, Info, Error - Default: All.
        Returns:
            JSON Response
        """
        data = {}
        for key, value in kwargs.items():
            data.update({key: value})
        path = "/api/log"
        res = self.request_get(path, **data)
        return res
