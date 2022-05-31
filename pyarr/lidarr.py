from typing import Any, Optional, Union

from requests import Response

from .base import BaseArrAPI
from .const import PAGE, PAGE_SIZE
from .exceptions import PyarrError, PyarrMissingProfile
from .models.common import PyarrSortDirection
from .models.lidarr import LidarrArtistMonitor, LidarrSortKeys


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
        defaultTags: list[int],
        qualityProfile: int,
        metadataProfile: int,
    ) -> dict[str, Any]:
        """Adds a root folder

        Args:
            name (str): Name for this root folder
            path (str): Location the files should be stored
            defaultTags (list[int]): List of default tag IDs
            qualityProfile (int): Default quality profile ID
            metadataProfile (int): Default metadata profile ID

        Returns:
            dict[str, Any]: Dictonary with added record
        """
        folder_json = {
            "defaultTags": defaultTags,
            "defaultQualityProfileId": qualityProfile,
            "defaultMetadataProfileId": metadataProfile,
            "name": name,
            "path": path,
        }

        return self._post("rootfolder", self.ver_uri, data=folder_json)

    def lookup(self, term: str) -> list[dict[str, Any]]:
        """Search for an artist / album / song

        Args:
            term (str): Search term

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("search", self.ver_uri, list, params={"term": term})

    def get_artist(self, id_: Union[str, int, None] = None) -> list[dict[str, Any]]:
        """Get an artist by ID or get all artists

        Args:
            id_ (Union[str, int, None], optional): Artist ID. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """

        _path = "" if isinstance(id_, str) or id_ is None else f"/{id_}"
        return self.assert_return(
            f"artist{_path}",
            self.ver_uri,
            list,
            params={"mbId": id_} if isinstance(id_, str) else None,
        )

    def _artist_json(
        self,
        term: str,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        artist_monitor: LidarrArtistMonitor = LidarrArtistMonitor.ALL_ALBUMS,
        artist_search_for_missing_albums: bool = False,
    ) -> dict[str, Any]:
        """Method to help build the JSON for adding an artist

        Args:
            term (str): Search term for artist
            root_dir (str): Root directory for music
            quality_profile_id (Optional[int], optional): Quality profile Id. Defaults to None.
            metadata_profile_id (Optional[int], optional): Metadata profile ID. Defaults to None.
            monitored (bool, optional): Should this be monitored. Defaults to True.
            artist_monitor (LidarrArtistMonitor, optional): Should the artist be monitored. Defaults to LidarrArtistMonitor.ALL_ALBUMS.
            artist_search_for_missing_albums (bool, optional): Should we search for missing albums. Defaults to False.

        Raises:
            PyarrMissingProfile: Raised when quality or metadata profile are missing

        Returns:
            dict[str, Any]: Dictionary with artist information
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
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        artist_monitor: LidarrArtistMonitor = LidarrArtistMonitor.ALL_ALBUMS,
        artist_search_for_missing_albums: bool = False,
    ) -> dict[str, Any]:
        """Adds an artist based on a search term, must be artist name or album/single
        by lidarr guid

        Args:
            search_term (str): Artist name or album/single
            root_dir (str): Directory for music to be stored
            quality_profile_id (Optional[int], optional): Quality profile ID. Defaults to None.
            metadata_profile_id (Optional[int], optional): Metadata profile ID. Defaults to None.
            monitored (bool, optional): Monitor the artist. Defaults to True.
            artist_monitor (LidarrArtistMonitor, optional): Monitor the artist. Defaults to LidarrArtistMonitor.ALL_ALBUMS.
            artist_search_for_missing_albums (bool, optional): Search for missing albums by this artist. Defaults to False.

        Returns:
            dict[str, Any]: Dictonary with added record
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
        return self._post("artist", self.ver_uri, data=artist_json)

    def upd_artist(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing artist

        Args:
            data (dict[str, Any]): Data for the artist record

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        return self._put("artist", self.ver_uri, data=data)

    def delete_artist(self, id_: int) -> Response:
        """Delete an artist with the provided ID

        Args:
            id_ (int): Artist ID to be deleted

        Returns:
            Response: 200 / 401
        """
        return self._delete(f"artist/{id_}", self.ver_uri)

    def lookup_artist(self, term: str) -> list[dict[str, Any]]:
        """Search for an Artist to add to the database

        Args:
            term (str): Search term to use for lookup

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """

        return self.assert_return(
            "artist/lookup", self.ver_uri, list, params={"term": term}
        )

    def get_album(
        self,
        albumIds: Union[int, list[int], None] = None,
        artistId: Optional[int] = None,
        foreignAlbumId: Optional[int] = None,
        allArtistAlbums: bool = False,
    ) -> list[dict[str, Any]]:
        """Get a specific album by ID, or get all albums

        Args:
            albumIds (Union[int, list[int], None], optional): Database album IDs. Defaults to None.
            artistId (Optional[int], optional): Database artist IDs. Defaults to None.
            foreignAlbumId (Optional[int], optional): Foreign album id. Defaults to None.
            allArtistAlbums (bool, optional): Get all artists albums. Defaults to False.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params: dict[str, Any] = {"includeAllArtistAlbums": str(allArtistAlbums)}

        if isinstance(albumIds, list):
            params["albumids"] = albumIds
        if artistId is not None:
            params["artistId"] = artistId
        if foreignAlbumId is not None:
            params["foreignAlbumId"] = foreignAlbumId
        _path = "" if isinstance(albumIds, list) or albumIds is None else f"/{albumIds}"
        return self.assert_return(f"album{_path}", self.ver_uri, list, params=params)

    def _album_json(
        self,
        term: str,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        artist_monitor: LidarrArtistMonitor = LidarrArtistMonitor.ALL_ALBUMS,
        artist_search_for_missing_albums: bool = False,
    ) -> dict[str, Any]:
        """Method to help build the JSON for adding an album

        Args:
            term (str): Search term for the album
            root_dir (str): Director to store the album.
            quality_profile_id (Optional[int], optional): Quality profile ID. Defaults to None.
            metadata_profile_id (Optional[int], optional): Metadata profile ID. Defaults to None.
            monitored (bool, optional): Monitor the albums. Defaults to True.
            artist_monitor (LidarrArtistMonitor, optional): Monitor the artist. Defaults to LidarrArtistMonitor.ALL_ALBUMS.
            artist_search_for_missing_albums (bool, optional): Search for missing albums by the artist. Defaults to False.

        Raises:
            PyarrMissingProfile: Error if there are no quality or metadata profiles that match

        Returns:
            dict[str, Any]: Dictionary with album data
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
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        artist_monitor: LidarrArtistMonitor = LidarrArtistMonitor.ALL_ALBUMS,
        artist_search_for_missing_albums: bool = False,
    ) -> dict[str, Any]:
        """Adds an album to Lidarr

        Args:
            search_term (str): Name of the album to search for
            root_dir (str): Location to store music
            quality_profile_id (Optional[int], optional): Quality profile ID. Defaults to None.
            metadata_profile_id (Optional[int], optional): Metadata profile ID. Defaults to None.
            monitored (bool, optional): Should the album be monitored. Defaults to True.
            artist_monitor (LidarrArtistMonitor, optional): What level to monitor the artist. Defaults to LidarrArtistMonitor.ALL_ALBUMS.
            artist_search_for_missing_albums (bool, optional): Search for any missing albums by this artist. Defaults to False.

        Returns:
            dict[str, Any]: Dictionary with added record
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
        return self._post("album", self.ver_uri, data=album_json)

    def upd_album(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update an album

        Args:
            data (dict[str, Any]): data to update albums

        Note:
            To be used in conjunction with get_album()

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        return self._put("album", self.ver_uri, data=data)

    def delete_album(self, id_: int) -> Response:
        """Delete an album with the provided ID

        Args:
            id_ (int): Album ID to be deleted

        Returns:
            Response: 200 / 401
        """
        return self._delete(f"album/{id_}", self.ver_uri)

    def lookup_album(self, term: str) -> list[dict[str, Any]]:
        """Search for an Album to add to the database

        Args:
            term (str): Search term to use for lookup

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return(
            "album/lookup", self.ver_uri, list, params={"term": term}
        )

    # POST /command
    def post_command(self) -> Any:
        """This function is not implemented

        Raises:
            NotImplementedError: Error
        """
        raise NotImplementedError("This feature is not implemented yet.")

    # GET /wanted
    def get_wanted(
        self,
        id_: Optional[int] = None,
        sort_key: LidarrSortKeys = LidarrSortKeys.TITLE,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_dir: PyarrSortDirection = PyarrSortDirection.ASC,
        missing: bool = True,
    ) -> dict[str, Any]:
        """Get wanted albums that are missing or not meeting cutoff

        Args:
            id_ (int | None, optional): Specific album ID to return. Defaults to None.
            sort_key (LidarrSortKeys, optional): id, title, ratings, or quality". (Others do not apply). Defaults to LidarrSortKeys.TITLE.
            page (int, optional): Page number to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_dir (PyarrSortDirection, optional): Sort ascending or descending. Defaults to PyarrSortDirection.ASC.
            missing (bool, optional): Search for missing (True) or cutoff not met (False). Defaults to True.

        Returns:
            dict[str, Any]: List of dictionaries with items
        """
        params = {
            "sortKey": sort_key.value,
            "page": page,
            "pageSize": page_size,
        }
        _path = "missing" if missing else "cutoff"
        return self.assert_return(
            f"wanted/{_path}{'' if id_ is None else f'/{id_}'}",
            self.ver_uri,
            dict,
            params=params,
        )

    # GET /parse
    # TODO: Confirm response type
    def get_parse(self, title: str) -> list[dict[str, Any]]:
        """Return the music / artist with a matching filename

        Args:
            title (str): file

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("parse", self.ver_uri, list, params={"title": title})

    # GET /track
    def get_tracks(
        self,
        artistId: Optional[int] = None,
        albumId: Optional[int] = None,
        albumReleaseId: Optional[int] = None,
        trackIds: Union[int, list[int], None] = None,
    ) -> list[dict[str, Any]]:
        """Get tracks based on provided IDs

        Args:
            artistId (Optional[int], optional): Artist ID. Defaults to None.
            albumId (Optional[int], optional): Album ID. Defaults to None.
            albumReleaseId (Optional[int], optional): Album Release ID. Defaults to None.
            trackIds (Union[int, list[int], None], optional): Track IDs. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params: dict[str, Any] = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["albumId"] = albumId
        if albumReleaseId is not None:
            params["albumReleaseId"] = albumReleaseId
        if isinstance(trackIds, list):
            params["trackIds"] = trackIds
        return self.assert_return(
            f"track{f'/{trackIds}' if isinstance(trackIds, int) else ''}",
            self.ver_uri,
            list,
            params=params,
        )

    # GET /trackfile/
    def get_track_file(
        self,
        artistId: Optional[int] = None,
        albumId: Optional[int] = None,
        trackFileIds: Union[int, list[int], None] = None,
        unmapped: bool = False,
    ) -> list[dict[str, Any]]:
        """Get track files based on IDs, or get all unmapped files

        Args:
            artistId (Optional[int], optional): Artist database ID. Defaults to None.
            albumId (Optional[int], optional): Album database ID. Defaults to None.
            trackFileIds (Union[int, list[int], None], optional): Specific file IDs. Defaults to None.
            unmapped (bool, optional): Get all unmapped filterExistingFiles. Defaults to False.

        Raises:
            PyarrError: Where no IDs or unmapped params provided

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
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
        params: dict[str, Any] = {"unmapped": str(unmapped)}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["albumId"] = albumId
        if isinstance(trackFileIds, list):
            params["trackFileIds"] = trackFileIds
        return self.assert_return(
            f"trackfile{f'/{trackFileIds}' if isinstance(trackFileIds, int) else ''}",
            self.ver_uri,
            list,
            params=params,
        )

    # PUT /trackfile/{id_}
    def upd_track_file(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update an existing track file

        Note:
            To be used in conjunction with get_track_file()

        Args:
            data (dict[str, Any]): Updated data for track files

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        return self._put("trackfile", self.ver_uri, data=data)

    # DEL /trackfile/{ids_}
    def delete_track_file(self, ids_: Union[int, list[int]]) -> Response:
        """Delete track files. Use integer for one file or list for mass deletion.

        Args:
            ids_ (Union[int, list[int]]): Single ID or list of IDs for files to delete

        Returns:
            Response: 200 / 401
        """
        return self._delete(
            f"trackfile/{'bulk' if isinstance(ids_, list) else f'{ids_}'}",
            self.ver_uri,
            data={"trackFileIds": ids_} if isinstance(ids_, list) else None,
        )

    # GET /metadataprofile/{id}
    def get_metadata_profile(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Gets all metadata profiles or specific one with id_

        Args:
            id_ (Optional[int], optional): Metadata profile id from database. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        _path = f"/{id_}" if id_ else ""
        response = self._get(f"metadataprofile{_path}", self.ver_uri)
        assert isinstance(response, list)
        return response

    # POST /metadataprofile
    def add_metadata_profile(self) -> Any:
        """This function is not implemented

        Raises:
            NotImplementedError: Error
        """
        raise NotImplementedError("This feature is not implemented yet.")

    # PUT /metadataprofile
    def upd_metadata_profile(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update a metadata profile

        Args:
            data (dict[str, Any]): Data containing metadata profile and changes

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        return self._put("metadataprofile", self.ver_uri, data=data)

    # GET /config/metadataProvider
    def get_metadata_provider(self) -> list[dict[str, Any]]:
        """Get metadata provider config (settings/metadata)

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("config/metadataProvider", self.ver_uri, list)

    # PUT /config/metadataprovider
    def upd_metadata_provider(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update metadata provider by providing json data update

        Note:
            To be used in conjunction with get_metadata_provider()

        Args:
            data (dict[str, Any]): Configuration data

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        return self._put("config/metadataProvider", self.ver_uri, data=data)

    # GET /queue
    def get_queue(
        self,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_key: LidarrSortKeys = LidarrSortKeys.TIMELEFT,
        unknown_artists: bool = False,
        include_artist: bool = False,
        include_album: bool = False,
    ) -> dict[str, Any]:
        """Get the queue of download_release

        Args:
            page (int, optional): Which page to load. Defaults to PAGE.
            page_size (int, optional): Number of items per page. Defaults to PAGE_SIZE.
            sort_key (LidarrSortKeys, optional): Key to sort by. Defaults to LidarrSortKeys.TIMELEFT.
            unknown_artists (bool, optional): Include unknown artists. Defaults to False.
            include_artist (bool, optional): Include Artists. Defaults to False.
            include_album (bool, optional): Include albums. Defaults to False.

        Returns:
            dict[str, Any]: List of dictionaries with items
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortKey": sort_key,
            "unknownArtists": unknown_artists,
            "includeAlbum": include_album,
            "includeArtist": include_artist,
        }

        return self.assert_return("queue", self.ver_uri, dict, params=params)

    # GET /queue/details
    def get_queue_details(
        self,
        artistId: Optional[int] = None,
        albumIds: Union[list[int], None] = None,
        include_artist: bool = False,
        include_album: bool = True,
    ) -> list[dict[str, Any]]:
        """Get queue details for artist or album

        Args:
            artistId (Optional[int], optional): Artist database ID. Defaults to None.
            albumIds (Union[list[int], None], optional): Album database ID. Defaults to None.
            include_artist (bool, optional): Include the artist. Defaults to False.
            include_album (bool, optional): Include the album. Defaults to True.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """

        params: dict[str, Any] = {
            "includeArtist": include_artist,
            "includeAlbum": include_album,
        }
        if artistId is not None:
            params["artistId"] = artistId
        if albumIds is not None:
            params["albumIds"] = albumIds

        return self.assert_return("queue/details", self.ver_uri, list, params=params)

    # GET /release
    def get_release(
        self, artistId: Optional[int] = None, albumId: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """Search indexers for specified fields.

        Args:
            artistId (Optional[int], optional): Artist ID from DB. Defaults to None.
            albumId (Optional[int], optional): Album IT from Database. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {}
        if artistId is not None:
            params["artistId"] = artistId
        if albumId is not None:
            params["artistId"] = albumId
        return self.assert_return("release", self.ver_uri, list, params=params)

    # GET /rename
    def get_rename(
        self, artistId: int, albumId: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """Get files matching specified id that are not properly renamed yet.

        Args:
            artistId (int): Database ID for Artists
            albumId (Optional[int], optional): Album ID. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {"artistId": artistId}
        if albumId is not None:
            params["albumId"] = albumId
        return self.assert_return(
            "rename",
            self.ver_uri,
            list,
            params=params,
        )

    # GET /manualimport
    def get_manual_import(
        self,
        downloadId: str,
        artistId: int = 0,
        folder: Optional[str] = None,
        filterExistingFiles: bool = True,
        replaceExistingFiles: bool = True,
    ) -> list[dict[str, Any]]:
        """Gets a manual import list

        Args:
            downloadId (str): Download IDs
            artistId (int, optional): Artist Database ID. Defaults to 0.
            folder (Optional[str], optional): folder name. Defaults to None.
            filterExistingFiles (bool, optional): filter files. Defaults to True.
            replaceExistingFiles (bool, optional): replace files. Defaults to True.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {
            "artistId": artistId,
            "downloadId": downloadId,
            "filterExistingFiles": str(filterExistingFiles),
            "folder": folder if folder is not None else "",
            "replaceExistingFiles": str(replaceExistingFiles),
        }
        return self.assert_return("manualimport", self.ver_uri, list, params=params)

    # PUT /manualimport
    def upd_manual_import(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update a manual import

        Note:
            To be used in conjunction with get_manual_import()

        Args:
            data (dict[str, Any]): Data containing changes

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        return self._put("manualimport", self.ver_uri, data=data)

    # GET /retag
    def get_retag(
        self, artistId: int, albumId: Optional[int] = None
    ) -> list[dict[str, Any]]:
        """Get Retag

        Args:
            artistId (int): ID for the  artist
            albumId Optional[int], optional): ID foir the album. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {"artistId": artistId}
        if albumId is not None:
            params["albumId"] = albumId
        return self.assert_return(
            "retag",
            self.ver_uri,
            list,
            params=params,
        )
