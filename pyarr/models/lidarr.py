from typing import Literal

LidarrCommand = Literal[
    "AlbumSearch",
    "ApplicationUpdateCheck",
    "ArtistSearch",
    "DownloadedAlbumsScan",
    "MissingAlbumSearch",
    "RefreshAlbum",
    "RefreshArtist",
]
"""
Lidarr commands.

    Note:
        The parameters are supplied as `**kwargs` within the `post_command` method.

DownloadedAlbumsScan:
    Scans downloaded albums for state

    Args:
        path (str): path to files

ArtistSearch:
    searches specified artist

    Args:
        artistId (int): ID of artist

RefreshArtist:
    Refreshes all of the artists, or specific by ID

    Args:
        artistId (int, Optional): ID of Album

RefreshAlbum:
    Refreshes all of the albums, or specific by ID

    Args:
        albumId (int, Optional): ID of Album

ApplicationUpdateCheck:
    Checks for Application updates

MissingAlbumSearch:
    Search for any missing albums

AlbumSearch:
    Search for albums

RssSync:
    Synchronise RSS Feeds

Backup:
    Backup the server data

"""

#: Lidarr sort keys.
LidarrSortKey = Literal[
    "albums.title",
    "artistId",
    "date",
    "downloadClient",
    "id",
    "indexer",
    "message",
    "path",
    "progress",
    "protocol",
    "quality",
    "ratings",
    "albums.releaseDate",
    "sourcetitle",
    "status",
    "timeleft",
    "title",
]


#: Lidarr Monitor types for an artist music
LidarrArtistMonitor = Literal["all", "future", "missing", "existing", "first", "latest"]


#: Import List schema implementations
LidarrImportListSchema = Literal[
    "LidarrImport",
    "HeadphonesImport",
    "LastFmTag",
    "LastFmUser",
    "LidarrLists",
    "MusicBrainzSeries",
    "SpotifyFollowedArtists",
    "SpotifyPlaylist",
    "SpotifySavedAlbums",
]

#: Lidarr History Sort Keys
LidarrHistorySortKey = Literal["sourceTitle", "status"]
