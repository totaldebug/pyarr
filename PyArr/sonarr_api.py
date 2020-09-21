# -*- coding: utf-8 -*-

from datetime import datetime

from .request_api import RequestAPI


class SonarrAPI(RequestAPI):
    def __init__(
        self,
        host_url: str,
        api_key: str,
    ):
        """Constructor requires Host-URL and API-KEY

        Args:
            host_url (str): Host url to sonarr.
            api_key: API key from Sonarr. You can find this
        """
        super().__init__(host_url, api_key)

    def getCalendar(self, *args):
        """getCalendar retrieves info about when series were/will be downloaded.
        If start and end are not provided, retrieves series airing today and tomorrow.

         args:
             start_date:
             end_date:

         Returns:
             json response

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
        else:
            print("no args")

        res = self.request_get(path, **data)
        return res.json()

    def getCommand(self, *args):
        """getCommand Queries the status of a previously
        started command, or all currently started commands.

        Args:
            Optional - id (int) Unique ID of command
        Returns:
            json response

        """
        if len(args) == 1:
            path = f"/api/command/{args[0]}"
        else:
            path = "/api/command"

        res = self.request_get(path)
        return res.json()

    def __setCommand(self, data):
        """Private Command Method

        Args:
            data (dict): data payload to send to /api/command

        Returns:
            json response
        """
        path = "/api/command"
        res = self.request_post(path, data)
        return res.json()

    def refreshSeries(self, *args):
        """RefreshSeries refreshes series information and rescans disk.

        Args:
            Optional - seriesId (int)
        Returns:
            json response

        """
        data = {}
        if len(args) == 1:
            data.update({"name": "RefreshSeries", "seriesId": args[0]})
        else:
            data.update({"name": "RefreshSeries"})
        return self.__setCommand(data)

    def rescanSeries(self, *args):
        """RescanSeries scans disk for any downloaded episodes for all or specified series.

        Args:
            Optional - seriesId (int)
        Returns:
            json response

        """
        data = {}
        if len(args) == 1:
            data.update({"name": "RescanSeries", "seriesId": args[0]})
        else:
            data.update({"name": "RescanSeries"})
        return self.__setCommand(data)

    def getDiskSpace(self):
        """GetDiskSpace retrieves info about the disk space on the server.

        Args:
            None
        Returns:
            json response

        """
        path = "/api/diskspace"
        res = self.request_get(path)
        return res.json()

    def getEpisodesBySeriesId(self, seriesId):
        """Returns all episodes for the given series

        Args:
            seriesId (int):
        Returns:
            json response
        """
        path = f"/api/episode?seriesId={seriesId}"
        res = self.request_get(path)
        return res.json()

    def getEpisodeByEpisodeId(self, episodeId):
        """Returns the episode with the matching id

        Args:
            episode_id (int):
        Returns:
            json response
        """
        path = f"/api/episode/{episodeId}"
        res = self.request_get(path)
        return res.json()

    def lookupSeries(self, term):
        """Searches for new shows on tvdb
        Args:
            Requried - term / tvdbId
        Returns:
            json response

        """
        term = str(term)
        if term.isdigit():
            term = f"tvdb:{term}"
        else:
            term = term.replace(" ", "%20")
        path = f"/api/series/lookup?term={term}"
        res = self.request_get(path)
        return res.json()

    def getRoot(self):
        """Returns the Root Folder"""
        path = "/api/rootfolder"
        res = self.request_get(path)
        return res.json()

    def getQualityProfiles(self):
        """Gets all quality profiles"""
        path = "/api/profile"
        res = self.request_get(path)
        return res.json()

    def constructSeriesJson(self, tvdbId, qualityProfileId):
        """Searches for new shows on trakt and returns Series json to add

        Args:
            Required - dbID, <tvdb id>
            Required - qualityProfileId (int)

        Return:
            JsonArray

        """
        res = self.lookupSeries(tvdbId)
        s_dict = res[0]

        # get root folder path
        root = self.getRoot()[0]["path"]
        series_json = {
            "title": s_dict["title"],
            "seasons": s_dict["seasons"],
            "path": root + s_dict["title"],
            "qualityProfileId": qualityProfileId,
            "seasonFolder": True,
            "monitored": True,
            "tvdbId": tvdbId,
            "images": s_dict["images"],
            "titleSlug": s_dict["titleSlug"],
            "addOptions": {
                "ignoreEpisodesWithFiles": True,
                "ignoreEpisodesWithoutFiles": True,
            },
        }
        return series_json

    def getSeries(self, *args):
        """Return all series in your collection or the series with the matching ID if one is found
        Args:
            Optional - seriesID

        Returns:
            Json Array
        """
        if len(args) == 1:
            path = f"/api/series/{args[0]}"
        else:
            path = "/api/series"

        res = self.request_get(path)
        return res.json()

    def addSeries(self, dbId, qualityProfileId):
        """Add a new series to your collection

        Args:
            Required - dbid
            Required - qualityProfileId
        Returns:
            json response

        """
        series_json = self.constructSeriesJson(dbId, qualityProfileId)

        path = "/api/series"
        res = self.request_post(path, data=series_json)
        return res.json()

    # TODO: Test
    def updSeries(self, data):
        """Update an existing series"""

        path = "/api/series"
        res = self.request_put(path, data=series_json)
        return res.json()

    def delSeries(self, seriesId, delFiles=False):
        """Delete the series with the given ID"""
        # File deletion does not work
        data = {"deleteFiles": delFiles}
        path = f"/api/series/{seriesId}"
        res = self.request_del(path, data)
        return res.json()

    def getSystemStatus(self):
        """Returns the System Status as json"""
        path = "/api/system/status"
        res = self.request_get(path)
        return res.json()

    def getQueue(self):
        """Gets current downloading info

        Returns:
            json Array
        """
        path = "/api/queue"
        res = self.request_get(path)
        return res.json()

    # TODO: requires Test
    def delQueue(self, id, *args):
        """Deletes an item from the queue and download client. Optionally blacklist item after deletion.

        Args:
            Required - id (int)
            Optional - blacklist (bool)
        Returns:
            json response
        """
        data = {}
        data.update({"id": id})
        if len(args) == 1:
            data.update(
                {
                    "blacklist": args[1],
                }
            )
        path = "/api/queue/"
        res = self.request_del(path, data)
        return res.json()

    def getWanted(self, **kwargs):
        """Gets Wanted / Missing episodes

        Args:
            Required - sortKey (string) - series.title or airDateUtc (default)
            Optional - page (int) - 1-indexed Default: 1
            Optional - pageSize (int) - Default: 10
            Optional - sortDir (string) - asc or desc - Default: asc
        Returns:
            json response
        """
        data = {}
        data.update({"sortKey": kwargs.get("sortKey", "airDateUtc")})
        for key, value in kwargs.items():
            data.update({key: value})
        path = "/api/wanted/missing"
        res = self.request_get(path, **data)
        return res.json()

    def getHistory(self, **kwargs):
        """Gets history (grabs/failures/completed)

        Args:
            Required - sortKey (string) - series.title or date (default)
            Optional - page (int) - 1-indexed
            Optional - pageSize (int) - Default: 0
            Optional - sortDir (string) - asc or desc - Default: asc
            Optional - episodeId (int) - Filters to a specific episode ID
        Returns:
            json response
        """
        data = {}
        data.update({"sortKey": kwargs.get("sortKey", "date")})
        for key, value in kwargs.items():
            data.update({key: value})
        path = "/api/history"
        res = self.request_get(path, **data)
        return res.json()

    def getLogs(self, **kwargs):
        """Gets Sonarr Logs

        Kwargs;
            Required - None
            Optional - page (int) - Page number - Default: 1.
            optional - pageSize (int) - How many records per page - Default: 10.
            optional - sortKey (str) - What key to sort on - Default: 'time'.
            optional - sortDir (str) - What direction to sort asc or desc - Default: desc.
            optional - filterKey (str) - What key to filter on - Default: None.
            optional - filterValue (str) - What to filter on (Warn, Info, Error, All) - Default: All.

        Returns:
            Json Array
        """
        data = {}
        for key, value in kwargs.items():
            data.update({key: value})
        path = "/api/log"
        res = self.request_get(path, **data)
        return res.json()

    def getBackup(self):
        """Returns the backups as json"""
        path = "/api/system/backup"
        res = self.request_get(path)
        return res.json()

    # TODO: Test this
    def updEpisode(self, data):
        """Update the given episodes, currently only monitored is changed, all
        other modifications are ignored. All parameters (you should perform a
        GET/{id} and submit the full body with the changes, as other values may
        be editable in the future.

            Args:
                data (dict): data payload

            Returns:
                json response
        """
        path = "/api/episode"
        res = self.request_put(path, data)
        return res.json()

    # TODO: Test this
    def get_episode_files_by_series_id(self, series_id):
        """Returns all episode files for the given series

        Args:
            series_id (int):

        Returns:
            requests.models.Response: Response object form requests.
        """
        data = {"seriesId": series_id}
        path = "/api/episodefile"
        res = self.request_get(path, **data)
        return res.json()

    # TODO: Test this
    def get_episode_file_by_episode_id(self, episode_id):
        """Returns the episode file with the matching id

        Kwargs:
            episode_id (int):

        Returns:
            requests.models.Response: Response object form requests.
        """
        path = "/api/episodefile/{}".format(episode_id)
        res = self.request_get(path)
        return res.json()

    # TODO: Test this
    def rem_episode_file_by_episode_id(self, episode_id):
        """Delete the given episode file

        Kwargs:
            episode_id (str):

        Returns:
            requests.models.Response: Response object form requests.
        """
        path = "/api/episodefile/{}".format(episode_id)
        res = self.request_del(path, data=None)
        return res.json()

    # TODO: Work in progress.
    def serach_selected(self):
        pass

    # TODO: Test this
    def push_release(self, **kwargs):
        """Notifies Sonarr of a new release.
        title: release name
        downloadUrl: .torrent file URL
        protocol: usenet / torrent
        publishDate: ISO8601 date string

        Kwargs:
            title (str):
            downloadUrl (str):
            protocol (str):
            publishDate (str):

        Returns:
            requests.models.Response: Response object form requests.
        """
        path = "/api/release/push"
        res = self.request_post(path, data=kwargs)
        return res.json()

    # TODO: Test this
    def get_series_by_series_id(self, series_id):
        """Return the series with the matching ID or 404 if no matching series
        is found

            Args:
                series_id (int):

            Returns:
                requests.models.Response: Response object form requests.
        """
        path = "/api/series/{}".format(series_id)
        res = self.request_get(path)
        return res.json()
