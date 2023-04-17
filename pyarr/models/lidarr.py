from typing import Literal

#: Lidarr commands.
LidarrCommand = Literal[
    "AlbumSearch",
    "ApplicationUpdateCheck",
    "ArtistSearch",
    "DownloadedAlbumsScan",
    "MissingAlbumSearch",
    "RefreshAlbum",
    "RefreshArtist",
]


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
