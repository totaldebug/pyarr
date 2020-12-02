# -*- coding: utf-8 -*-

from datetime import datetime

from .request_api import RequestAPI


class RadarrAPIv3(RequestAPI):
    def __init__(
        self,
        host_url: str,
        api_key: str,
    ):
        """Constructor requires Host-URL and API-KEY

        Args:
            host_url (str): Host url to radarr.
            api_key: API key from Radarr. You can find this
        """
        super().__init__(host_url, api_key)

    ## Movies
    # TODO: GET Movie
    # TODO: POST Movie
    # TODO: PUT Movie
    # TODO: DELETE Movie
    # TODO: GET Movie Lookup
    # TODO: PUT Movie Editor
    # TODO: DELETE Movie Editor
    # TODO: POST Movie import

    ## Movie Files
    # TODO: GET movieFiles
    # TODO: GET Movie File
    # TODO: DELETE Movie Files

    ## history
    # TODO: GET history
    # TODO: GET History Movies

    ## blacklist
    # TODO: GET blacklist
    # TODO: DELETE blacklist
    # TODO: GET blacklist movie
    # TODO: DELETE Blacklist Bulk

    ## queue
    # TODO: GET Queue

    ## indexer
    # TODO: GET indexer
    # TODO: GET Indexer by ID
    # TODO: PUT Indexer by id
    # TODO: DELETE Indexer by id

    ## Download client

    ## Import Lists

    ## Notification

    ## Tag

    ## diskspace

    ## Settings

    ## metadata

    ## system

    ## health
    def get_health(self):
        """Query radarr for health information"""
        path = "/api/v3/health"
        res = self.request_get(path)
        return res.json()

    ## command
    def post_command(self, **kwargs):
        """Performs any of the predetermined Radarr command routines.

        Kwargs:
            Required - name (string).

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
                    - movieIds:int[] - Specify a list of ids (comma separated) for individual movies to refresh

            See https://radarr.video/docs/api/#/Command/post-command
        Returns:
        json response

        """
        path = "/api/v3/command"

        data = kwargs
        res = self.request_post(path, data)
        return res.json()

    ## update
    def get_update(self):
        """Returns a list of recent updates to Radarr

        Location: System > Updates
        """
        path = "/api/v3/update"
        res = self.reuqest_get(path)
        return res.json()

    ## quality
    def get_quality_profiles(self):
        """Query Radarr for quality profiles"""
        path = "/api/v3/qualityProfile"
        res = self.reuqest_get(path)
        return res.json()

    ## calendar

    ## custom filters

    ## remote path mapping
