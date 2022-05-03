from .base import BaseArrAPI
from .const import PAGE, PAGE_SIZE


class SonarrAPI(BaseArrAPI):
    """API wrapper for Sonarr endpoints."""

    def __init__(self, host_url: str, api_key: str, ver_uri: str = ""):
        """Initialize the Sonarr API.

        Args:
            host_url (str): URL for Sonarr
            api_key (str): API key for Sonarr
            ver_uri (str): Version URI for Radarr. Defaults to None (empty string).
        """

        super().__init__(host_url, api_key, ver_uri)

    def _series_json(
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

        return {
            "title": series["title"],
            "seasons": series["seasons"],
            "rootFolderPath": root_dir,
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

    ## COMMAND

    # GET /command
    def get_command(self, id_=None):
        """Queries the status of a previously started command, or all currently started commands.

        Args:
            id_ (int, optional): Database id of the command. Defaults to None.

        Returns:
            JSON: Array
        """
        path = f"command/{id_}" if id_ else "command"
        return self.request_get(path, self.ver_uri)

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
        path = "command"
        data = {
            "name": name,
            **kwargs,
        }
        return self.request_post(path, self.ver_uri, data=data)

    ## EPISODE

    # GET /episode
    def get_episodes_by_series_id(self, id_):
        """Gets all episodes from a given series ID

        Args:
            id_ (int): Database id for series

        Returns:
            JSON: Array
        """
        path = "episode"
        params = {"seriesId": id_}
        return self.request_get(path, self.ver_uri, params=params)

    # GET /episode/{id}
    def get_episode_by_episode_id(self, id_):
        """Gets a specific episode by database id

        Args:
            id_ (int): Database id for episode

        Returns:
            JSON: Array
        """
        path = f"episode/{id_}"
        return self.request_get(path, self.ver_uri)

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
        path = "episode"
        return self.request_put(path, self.ver_uri, data=data)

    ## EPISODE FILE

    # GET /episodefile
    def get_episode_files_by_series_id(self, id_):
        """Returns all episode file information for series id specified

        Args:
            id_ (int): Database id of series

        Returns:
            JSON: Array
        """
        path = "episodefile"
        params = {"seriesId": id_}
        return self.request_get(path, self.ver_uri, params=params)

    # GET /episodefile/{id}
    def get_episode_file(self, id_):
        """Returns episode file information for specified id

        Args:
            id_ (int): Database id of episode file

        Returns:
            JSON: Array
        """
        path = f"episodefile/{id_}"
        return self.request_get(path, self.ver_uri)

    # DELETE /episodefile/{id}
    def del_episode_file(self, id_):
        """Deletes the episode file with corresponding id

        Args:
            id_ (int): Database id for episode file

        Returns:
            JSON: {}
        """
        path = f"episodefile/{id_}"
        return self.request_del(path, self.ver_uri)

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
        path = f"episodefile/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    def get_wanted(
        self, sort_key="airDateUtc", page=PAGE, page_size=PAGE_SIZE, sort_dir="asc"
    ):
        """Gets missing episode (episodes without files)

        Args:
            sort_key (str, optional): series.titke or airDateUtc. Defaults to "airDateUtc".
            page (int, optional): Page number to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_dir (str, optional): Direction to sort the items. Defaults to "asc".

        Returns:
            JSON: Array
        """
        path = "wanted/missing"
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDir": sort_dir,
        }
        return self.request_get(path, self.ver_uri, params=params)

    ## QUEUE

    # GET /queue
    def get_queue(self):
        """Gets currently downloading info

        Returns:
            JSON: Array
        """
        path = "queue"
        return self.request_get(path, self.ver_uri)

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
        path = "parse"
        return self.request_get(path, self.ver_uri, params=params)

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
        path = "parse"
        return self.request_get(path, self.ver_uri, params=params)

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
        path = "release"
        return self.request_get(path, self.ver_uri, params=params)

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
        path = "release"
        return self.request_post(path, self.ver_uri, data=data)

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
        path = "release/push"
        return self.request_post(path, self.ver_uri, data=data)

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
        path = f"series/{id_}" if id_ else "series"
        return self.request_get(path, self.ver_uri)

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
        series_json = self._series_json(
            tvdb_id,
            quality_profile_id,
            root_dir,
            season_folder,
            monitored,
            ignore_episodes_with_files,
            ignore_episodes_without_files,
            search_for_missing_episodes,
        )

        path = "series"
        return self.request_post(path, self.ver_uri, data=series_json)

    # PUT /series
    def upd_series(self, data):
        """Update an existing series

        Args:
            data (dict): contains data obtained by get_series()

        Returns:
            JSON: Array
        """
        path = "series"
        return self.request_put(path, self.ver_uri, data=data)

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
        path = f"series/{id_}"
        return self.request_del(path, self.ver_uri, params=params)

    # GET /series/lookup
    def lookup_series(self, term):
        """Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

        Args:
            term (str): Series' Name, using `%20` to signify spaces, as in `The%20Blacklist`

        Returns:
            JSON: Array
        """
        params = {"term": term}
        path = "series/lookup"
        return self.request_get(path, self.ver_uri, params=params)

    # GET /series/lookup
    def lookup_series_by_tvdb_id(self, id_):
        """Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

        Args:
            id_ (int): TVDB ID

        Returns:
            JSON: Array
        """
        params = {"term": f"tvdb:{id_}"}
        path = "series/lookup"
        return self.request_get(path, self.ver_uri, params=params)
