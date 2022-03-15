from enum import Enum
from typing import Dict, List, Union

from .base import BaseArrAPI
from .const import PAGE, PAGE_SIZE
from .exceptions import PyarrError, PyarrMissingProfile


class LidarrSortKeys(str, Enum):
    """Lidarr sort keys."""

    ALBUM_TITLE = "albums.title"
    ARTIST_ID = "artistId"
    DATE = "date"
    DOWNLOAD_CLIENT = "downloadClient"
    ID = "id"
    INDEXER = "indexer"
    MESSAGE = "message"
    PATH = "path"
    PROGRESS = "progress"
    PROTOCOL = "protocol"
    QUALITY = "quality"
    RATINGS = "ratings"
    RELEASE_DATE = "albums.releaseDate"
    SOURCE_TITLE = "sourcetitle"
    STATUS = "status"
    TIMELEFT = "timeleft"
    TITLE = "title"


class LidarrArtistMonitor(str, Enum):
    """Lidarr Monitor types for an artist music"""

    ALL_ALBUMS = "all"
    FUTURE_ALBUMS = "future"
    MISSING_ALBUMS = "missing"
    EXISTING_ALBUMS = "existing"
    FIRST_ALBUM = "first"
    LATEST_ALBUM = "latest"


class LidarrAPI(BaseArrAPI):
    """API wrapper for Lidarr endpoints.

    Args:
        RequestAPI (:obj:`str`): provides connection to API endpoint
    """

    def __init__(self, host_url: str, api_key: str):
        """Initialise Lidarr API

        Args:
            host_url (str): URL for Lidarr
            api_key (str): API key for Lidarr
        """

        ver_uri = "/v1"
        super().__init__(host_url, api_key, ver_uri)

    # POST /rootfolder
    def add_root_folder(
        self,
        name: str,
        path: str,
        defaultTags: List[int],
        qualityProfile: int,
        metadataProfile: int,
    ):
        """Adds a root folder

        Args:
            name (str): Name for this root folder
            path (str): Location the files should be stored
            defaultTags (List[int]): list of default tag IDs
            qualityProfile (int): default quality profile ID
            metadataProfile (int): default metadata profile ID

        Returns:
            JSON: Array
        """
        folder_json = {
            "defaultTags": defaultTags,
            "defaultQualityProfileId": qualityProfile,
            "defaultMetadataProfileId": metadataProfile,
            "name": name,
            "path": path,
        }

        return self.request_post("rootfolder", self.ver_uri, data=folder_json)

    def lookup(self, term: str):
        """Search for an artist / album / song

        Args:
            term (str): Search term

        Returns:
            JSON: Array
        """

        return self.request_get("search", self.ver_uri, params={"term": term})

    def get_artist(self, id_: Union[str, int, None] = None):
        """Get an artist by ID or get all artists

        Args:
            id_ (str | int | None, optional): Artist ID. Defaults to None.

        Returns:
            JSON: Array
        """

        _path = "" if isinstance(id_, str) or id_ is None else f"/{id_}"
        return self.request_get(
            f"artist{_path}",
            self.ver_uri,
            params={"mbId": id_} if isinstance(id_, str) else None,
        )

    def _artist_json(
        self,
        term: str,
        root_dir: str,
        quality_profile_id: Union[int, None] = None,
        metadata_profile_id: Union[int, None] = None,
        monitored: bool = True,
        artist_monitor: LidarrArtistMonitor = LidarrArtistMonitor.ALL_ALBUMS,
        artist_search_for_missing_albums: bool = False,
    ):
        """method to help build the JSON for adding an artist

        Args:
            term (str): Search term for artist
            root_dir (str): root directory for music
            quality_profile_id (Union[int, None], optional): Quality profile Id. Defaults to None.
            metadata_profile_id (Union[int, None], optional): Metadata profile ID. Defaults to None.
            monitored (bool, optional): Should this be monitored. Defaults to True.
            artist_monitor (LidarrArtistMonitor, optional): should the artist be monitored. Defaults to LidarrArtistMonitor.ALL_ALBUMS.
            artist_search_for_missing_albums (bool, optional): should we search for missing albums. Defaults to False.

        Raises:
            PyarrMissingProfile: Raised when quality or metadata profile are missing

        Returns:
            JSON: Array
        """
        if quality_profile_id is None:
            try:
                quality_profile_id = self.get_quality_profile()[0]["id"]
            except IndexError as exception:
                raise PyarrMissingProfile(
                    "There is no Quality Profile setup"
                ) from exception
        if metadata_profile_id is None:
            try:
                metadata_profile_id = self.get_metadata_profile()[0]["id"]
            except IndexError as exception:
                raise PyarrMissingProfile(
                    "There is no Metadata Profile setup"
                ) from exception

        artist = self.lookup_artist(term)[0]
        artist["id"] = 0
        artist["metadataProfileId"] = metadata_profile_id
        artist["qualityProfileId"] = quality_profile_id
        artist["rootFolderPath"] = root_dir
        artist["addOptions"] = {
            "monitor": artist_monitor,
            "searchForMissingAlbums": artist_search_for_missing_albums,
        }
        artist["monitored"] = monitored

        return artist

    def add_artist(
        self,
        search_term: str,
        root_dir: str,
        quality_profile_id: Union[int, None] = None,
        metadata_profile_id: Union[int, None] = None,
        monitored: bool = True,
        artist_monitor: LidarrArtistMonitor = LidarrArtistMonitor.ALL_ALBUMS,
        artist_search_for_missing_albums: bool = False,
    ):
        """Adds an artist based on a search term, must be artist name or album/single
        by lidarr guid

        Args:
            search_term (str): Artist name or album/single
            root_dir (str): Directory for music to be stored
            quality_profile_id (Union[int, None], optional): Quality profile id. Defaults to None.
            metadata_profile_id (Union[int, None], optional): Metadata profile id_. Defaults to None.
            monitored (bool, optional): monitor the artist. Defaults to True.
            artist_monitor (LidarrArtistMonitor, optional): [description]. Defaults to LidarrArtistMonitor.ALL_ALBUMS.
            artist_search_for_missing_albums (bool, optional): Search for missing albums by this artist. Defaults to False

        Returns:
            JSON: Array
        """

        artist_json = self._artist_json(
            search_term,
            root_dir,
            quality_profile_id,
            metadata_profile_id,
            monitored,
            artist_monitor,
            artist_search_for_missing_albums,
        )
        return self.request_post("artist", self.ver_uri, data=artist_json)

    def upd_artist(self, data):
        """Update an existing artist

        Note:
            To be used in conjunction with get_artist()

        Args:
            data (json): JSON data for the artist record

        Returns:
            JSON: Array
        """
        return self.request_put("artist", self.ver_uri, data=data)

    def delete_artist(self, id_: int):
        """Delete an artist with the provided ID

        Args:
            id_ (int): Artist ID to be deleted

        Returns:
            None
        """
        return self.request_del(f"artist/{id_}", self.ver_uri)

    def lookup_artist(self, term: str):
        """Search for an Artist to add to the database

        Args:
            term (str): search term to use for lookup

        Returns:
            JSON: Array
        """
        return self.request_get("artist/lookup", self.ver_uri, params={"term": term})

    def get_album(
        self,
        albumIds: Union[int, List[int], None] = None,
        artistId: Union[int, None] = None,
        foreignAlbumId: Union[int, None] = None,
        allArtistAlbums: bool = False,
    ):
        """Get a specific album by ID, or get all albums

        Args:
            albumIds (int | List[int] | None, optional): database album ids. Defaults to None.
            artistId (int | None, optional): database artist ids. Defaults to None.
            foreignAlbumId (int | None, optional): foreign album id. Defaults to None.
            allArtistAlbums (bool, optional): get all artists albums. Defaults to False.

        Returns:
            JSON: Array
        """
        params: Dict[str, Union[str, int, List[int]]] = {
            "includeAllArtistAlbums": str(allArtistAlbums)
        }

        if isinstance(albumIds, list):
            params["albumids"] = albumIds
        if artistId is not None:
            params["artistId"] = artistId
        if foreignAlbumId is not None:
            params["foreignAlbumId"] = foreignAlbumId
        _path = "" if isinstance(albumIds, list) or albumIds is None else f"/{albumIds}"
        return self.request_get(f"album{_path}", self.ver_uri, params=params)

    def _album_json(
        self,
        term: str,
        root_dir: str,
        quality_profile_id: Union[int, None] = None,
        metadata_profile_id: Union[int, None] = None,
        monitored: bool = True,
        artist_monitor: LidarrArtistMonitor = LidarrArtistMonitor.ALL_ALBUMS,
        artist_search_for_missing_albums: bool = False,
    ):
        """method to help build the JSON for adding an album

        Args:
            term (str): Search term for the album
            root_dir (str): Director to store the album.
            quality_profile_id (Union[int, None], optional): quality profile id. Defaults to None.
            metadata_profile_id (Union[int, None], optional): metadata profile id. Defaults to None.
            monitored (bool, optional): monitor the albums. Defaults to True.
            artist_monitor (LidarrArtistMonitor, optional): monitor the artist. Defaults to LidarrArtistMonitor.ALL_ALBUMS.
            artist_search_for_missing_albums (bool, optional): search for missing albums by the artist. Defaults to False.

        Raises:
            PyarrMissingProfile: Error if there are no quality or metadata profiles that match

        Returns:
            JSON: Array
        """
        if quality_profile_id is None:
            try:
                quality_profile_id = self.get_quality_profile()[0]["id"]
            except IndexError as exception:
                raise PyarrMissingProfile(
                    "There is no Quality Profile setup"
                ) from exception
        if metadata_profile_id is None:
            try:
                metadata_profile_id = self.get_metadata_profile()[0]["id"]
            except IndexError as exception:
                raise PyarrMissingProfile(
                    "There is no Metadata Profile setup"
                ) from exception

        artist = self.lookup_artist(term)[0]
        artist["id"] = 0
        artist["metadataProfileId"] = metadata_profile_id
        artist["qualityProfileId"] = quality_profile_id
        artist["rootFolderPath"] = root_dir
        artist["addOptions"] = {
            "monitor": artist_monitor,
            "searchForMissingAlbums": artist_search_for_missing_albums,
        }
        artist["monitored"] = monitored

        return artist

    def add_album(
        self,
        search_term: str,
        root_dir: str,
        quality_profile_id: Union[int, None] = None,
        metadata_profile_id: Union[int, None] = None,
        monitored: bool = True,
        artist_monitor: LidarrArtistMonitor = LidarrArtistMonitor.ALL_ALBUMS,
        artist_search_for_missing_albums: bool = False,
    ):
        """Adds an album to Lidarr

        Args:
            search_term (str): name of the album to search for
            root_dir (str): location to store music
            quality_profile_id (Union[int, None], optional): Quality profile Id. Defaults to None.
            metadata_profile_id (Union[int, None], optional): Metadata profile Id. Defaults to None.
            monitored (bool, optional): should the album be monitored. Defaults to True.
            artist_monitor (LidarrArtistMonitor, optional): what level to monitor the artist. Defaults to LidarrArtistMonitor.ALL_ALBUMS.
            artist_search_for_missing_albums (bool, optional): search for any missing albums by this artist. Defaults to False.

        Returns:
            JSON: Array
        """
        album_json = self._album_json(
            search_term,
            root_dir,
            quality_profile_id,
            metadata_profile_id,
            monitored,
            artist_monitor,
            artist_search_for_missing_albums,
        )
        return self.request_post("album", self.ver_uri, data=album_json)

    def upd_album(self, data):
        """Update an album

        Args:
            data (json): data ti update albums

        Note:
            To be used in conjunction with get_album()

        Returns:
            JSON: Array
        """
        return self.request_put("album", self.ver_uri, data=data)

    def delete_album(self, id_: int):
        """Delete an album with the provided ID

        Args:
            id_ (int): Album ID to be deleted

        Returns:
            None
        """
        return self.request_del(f"album/{id_}", self.ver_uri)

    def lookup_album(self, term: str):
        """Search for an Album to add to the database

        Args:
            term (str): search term to use for lookup

        Returns:
            JSON: Array
        """
        return self.request_get("album/lookup", self.ver_uri, params={"term": term})

    # POST /command
    def post_command(self):
        """This function is not implemented

        Raises:
            NotImplementedError: Error
        """
        raise NotImplementedError("This feature is not implemented yet.")

    # GET /wanted
    def get_wanted(
        self,
        id_: Union[int, None] = None,
        sort_key: LidarrSortKeys = LidarrSortKeys.TITLE,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_dir: str = "asc",
        missing: bool = True,
    ):
        """Get wanted albums that are missing or not meeting cutoff

        Args:
            id_ (int | None, optional): Specific album ID to return. Defaults to None.
            sort_key (LidarrSortKeys, optional): id, title, ratings or quality. Defaults to LidarrSortKeys.TITLE.
            page (int, optional): Page number to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_dir (str, optional): Sort ascending or descending. Defaults to "asc".
            missing (bool, optional): search for missing (True) or cutoff not met (False). Defaults to True.

        Returns:
            JSON: Array
        """
        params = {
            "sortKey": sort_key.value,
            "page": page,
            "pageSize": page_size,
        }
        _path = "missing" if missing else "cutoff"
        return self.request_get(
            f"wanted/{_path}{'' if id_ is None else f'/{id_}'}",
            self.ver_uri,
            params=params,
        )

    # GET /parse
    def get_parse(self, title: str):
        """Return the music / artist with a matching filename

        Args:
            title (str): file

        Returns:
            JSON: Array
        """
        return self.request_get("parse", self.ver_uri, params={"title": title})

    # GET /track
    def get_tracks(
        self,
        artistId: Union[int, None] = None,
        albumId: Union[int, None] = None,
        albumReleaseId: Union[int, None] = None,
        trackIds: Union[int, List[int], None] = None,
    ):
        """Get tracks based on provided IDs

        Args:
            artistId (int | None, optional): Artist ID. Defaults to None.
            albumId (int | None, optional): Album ID. Defaults to None.
            albumReleaseId (int | None, optional): Album Release ID. Defaults to None.
            trackIds (int | list[int] | None, optional): Track IDs. Defaults to None.

        Returns:
            JSON: Array
        """
        params: Dict[str, Union[int, List[int]]] = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["albumId"] = albumId
        if albumReleaseId is not None:
            params["albumReleaseId"] = albumReleaseId
        if isinstance(trackIds, list):
            params["trackIds"] = trackIds
        return self.request_get(
            f"track{f'/{trackIds}' if isinstance(trackIds, int) else ''}",
            self.ver_uri,
            params=params,
        )

    # GET /trackfile/
    def get_track_file(
        self,
        artistId: Union[int, None] = None,
        albumId: Union[int, None] = None,
        trackFileIds: Union[int, List[int], None] = None,
        unmapped: bool = False,
    ):
        """Get track files based on IDs, or get all unmapped files

        Args:
            artistId (Union[int, None], optional): Artist database ID. Defaults to None.
            albumId (Union[int, None], optional): Album database ID. Defaults to None.
            trackFileIds (Union[int, List[int], None], optional): specific file ids. Defaults to None.
            unmapped (bool, optional): get all unmapped filterExistingFiles. Defaults to False.

        Raises:
            PyarrError: where no IDs or unmapped params provided

        Returns:
            JSON: Array
        """
        if (
            artistId is None
            and albumId is None
            and trackFileIds is None
            and not unmapped
        ):
            raise PyarrError(
                "BadRequest: artistId, albumId, trackFileIds or unmapped must be provided"
            )
        params: Dict[str, Union[str, int, List[int]]] = {"unmapped": str(unmapped)}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["albumId"] = albumId
        if isinstance(trackFileIds, list):
            params["trackFileIds"] = trackFileIds
        return self.request_get(
            f"trackfile{f'/{trackFileIds}' if isinstance(trackFileIds, int) else ''}",
            self.ver_uri,
            params=params,
        )

    # PUT /trackfile/{id_}
    def upd_track_file(self, data):
        """Update an existing track file

        Note:
            To be used in conjunction with get_track_file()

        Args:
            data (json): updated data for track files

        Returns:
            JSON: Array
        """
        return self.request_put("trackfile", self.ver_uri, data=data)

    # DEL /trackfile/{ids_}
    def delete_track_file(self, ids_: Union[int, List[int]]):
        """Delete track files. Use integer for one file or list for mass deletion.

        Args:
            ids_ (int | list[int]): single ID or list of IDs for files to delete

        Returns:
            None
        """
        return self.request_del(
            f"trackfile/{'bulk' if isinstance(ids_, list) else f'{ids_}'}",
            self.ver_uri,
            data={"trackFileIds": ids_} if isinstance(ids_, list) else None,
        )

    # GET /metadataprofile/{id}
    def get_metadata_profile(self, id_: Union[int, None] = None):
        """Gets all metadata profiles or specific one with id_

        Args:
            id_ (int, optional): metadata profile id from database. Defaults to None.

        Returns:
            JSON: Array
        """
        _path = f"/{id_}" if id_ else ""
        return self.request_get(f"metadataprofile{_path}", self.ver_uri)

    # POST /metadataprofile
    def add_metadata_profile(self):
        """This function is not implemented

        Raises:
            NotImplementedError: Error
        """
        raise NotImplementedError("This feature is not implemented yet.")

    # PUT /metadataprofile
    def upd_metadata_profile(self, data):
        """Update a metadata profile

        Args:
            data (json): data containing metadata profile and changes

        Returns:
            JSON: Array
        """
        return self.request_put("metadataprofile", self.ver_uri, data=data)

    # GET /config/metadataProvider
    def get_metadata_provider(self):
        """Get metadata provider config (settings/metadata)

        Returns:
            JSON: Array
        """
        return self.request_get("config/metadataProvider", self.ver_uri)

    # PUT /config/metadataprovider
    def upd_metadata_provider(self, data):
        """Update metadata provider by providing json data update

        Note:
            To be used in conjunction with get_metadata_provider()

        Args:
            data (json): configuration data as json

        Returns:
            JSON: Array
        """
        return self.request_put("config/metadataProvider", self.ver_uri, data=data)

    # GET /queue
    def get_queue(
        self,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_key: LidarrSortKeys = LidarrSortKeys.TIMELEFT,
        unknown_artists: bool = False,
        include_artist: bool = False,
        include_album: bool = False,
    ):
        """Get the queue of download_release

        Args:
            page (int, optional): Which page to load. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_key (LidarrSortKeys, optional): Key to sort by. Defaults to LidarrSortKeys.TIMELEFT.
            unknown_artists (bool, optional): include unknown artists. Defaults to False.
            include_artist (bool, optional): Include Artists. Defaults to False.
            include_album (bool, optional): Include albums. Defaults to False.

        Returns:
            JSON: Array
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortKey": sort_key,
            "unknownArtists": unknown_artists,
            "includeAlbum": include_album,
            "includeArtist": include_artist,
        }

        return self.request_get("queue", self.ver_uri, params=params)

    # GET /queue/details
    def get_queue_details(
        self,
        artistId: Union[int, None] = None,
        albumIds: Union[List[int], None] = None,
        include_artist: bool = False,
        include_album: bool = True,
    ):
        """Get queue details for artist or album

        Args:
            artistId (Union[int, None], optional): Artist database ID. Defaults to None.
            albumIds (Union[List[int], None], optional): Album database ID. Defaults to None.
            include_artist (bool, optional): Include the artist. Defaults to False.
            include_album (bool, optional): Include the album. Defaults to True.

        Returns:
            JSON: Array
        """

        params: dict = {
            "includeArtist": include_artist,
            "includeAlbum": include_album,
        }
        if artistId is not None:
            params["artistId"] = artistId
        if albumIds is not None:
            params["albumIds"] = albumIds

        return self.request_get("queue/details", self.ver_uri, params=params)

    # GET /release
    def get_release(
        self, artistId: Union[int, None] = None, albumId: Union[int, None] = None
    ):
        """Search indexers for specified fields.

        Args:
            artistId (Union[int, None], optional): Artist ID from DB. Defaults to None.
            albumId (Union[int, None], optional): Album IT from Database. Defaults to None.

        Returns:
            JSON: Array
        """
        params = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["artistId"] = albumId
        return self.request_get("release", self.ver_uri, params=params)

    # GET /rename
    def get_rename(self, artistId: int, albumId: Union[int, None] = None):
        """Get files matching specified id that are not properly renamed yet.

        Args:
            artistId (int): Database ID for Artists
            albumId (Union[int, None], optional): Album ID. Defaults to None.

        Returns:
            JSON: Array
        """
        params = {"artistId": artistId}
        if albumId is not None:
            params["albumId"] = albumId
        return self.request_get(
            "rename",
            self.ver_uri,
            params=params,
        )

    # GET /manualimport
    def get_manual_import(
        self,
        downloadId: str,
        artistId: int = 0,
        folder: Union[str, None] = None,
        filterExistingFiles: bool = True,
        replaceExistingFiles: bool = True,
    ):
        """Gets a manual import list

        Args:
            downloadId (str): Download IDs
            artistId (int, optional): Artist Database ID. Defaults to 0.
            folder (Union[str, None], optional): folder name. Defaults to None.
            filterExistingFiles (bool, optional): filter files. Defaults to True.
            replaceExistingFiles (bool, optional): replace files. Defaults to True.

        Returns:
            JSON: Array
        """
        params = {
            "artistId": artistId,
            "downloadId": downloadId,
            "filterExistingFiles": str(filterExistingFiles),
            "folder": folder if folder is not None else "",
            "replaceExistingFiles": str(replaceExistingFiles),
        }
        return self.request_get("manualimport", self.ver_uri, params=params)

    # PUT /manualimport
    def upd_manual_import(self, data):
        """Update a manual import

        Note:
            To be used in conjunction with get_manual_import()

        Args:
            data (json): json data containing changes

        Returns:
            JSON: Array
        """
        return self.request_put("manualimport", self.ver_uri, data=data)

    # GET /retag
    def get_retag(self, artistId: int, albumId: Union[int, None] = None):
        """Get Retag

        Args:
            artistId (int): ID for the  artist
            albumId Union[int, None], optional): ID foir the album. Defaults to None.

        Returns:
            JSON: Array
        """
        params = {"artistId": artistId}
        if albumId is not None:
            params["albumId"] = albumId
        return self.request_get(
            "retag",
            self.ver_uri,
            params=params,
        )
