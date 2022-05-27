from enum import Enum


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


class LidarrCommands(str, Enum):
    """Lidarr commands."""

    ALBUM_SEARCH = "AlbumSearch"
    APP_UPDATE_CHECK = "ApplicationUpdateCheck"
    ARTIST_SEARCH = "ArtistSearch"
    DOWNLOADED_ALBUMS_SCAN = "DownloadedAlbumsScan"
    MISSING_ALBUM_SEARCH = "MissingAlbumSearch"
    REFRESH_ALBUM = "RefreshAlbum"
    REFRESH_ARTIST = "RefreshArtist"
