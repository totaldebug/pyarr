from typing import Literal

# --- Common Literals ---

#: Pyarr sort direction
PyarrSortDirection = Literal["ascending", "default", "descending"]

#: Log filter keys
PyarrLogFilterKey = Literal["level"]

#: Log filter values
PyarrLogFilterValue = Literal["all", "info", "warn", "error"]

#: Log Sort Keys
PyarrLogSortKey = Literal["Id", "level", "time", "logger", "message", "exception", "exceptionType"]

#: Block list sort keys
PyarrBlocklistSortKey = Literal["date"]

#: History sort keys
PyarrHistorySortKey = Literal[
    "id",
    "date",
    "eventType",
    "series.title",
    "movieFile.relativePath",
    "sourceTitle",
    "status",
]

#: Task sort keys
PyarrTaskSortKey = Literal["timeleft"]

#: Notification schema implementations
PyarrNotificationSchema = Literal[
    "Apprise",
    "CustomScript",
    "Discord",
    "Email",
    "MediaBrowser",
    "Gotify",
    "Join",
    "Xbmc",
    "MailGun",
    "Notifiarr",
    "Ntfy",
    "PlexServer",
    "Prowl",
    "PushBullet",
    "Pushcut",
    "Pushover",
    "SendGrid",
    "Signal",
    "Simplepush",
    "Slack",
    "SynologyIndexer",
    "Telegram",
    "Trakt",
    "Twitter",
    "Webhook",
]

#: Download client schema implementations
PyarrDownloadClientSchema = Literal[
    "Aria2",
    "Deluge",
    "TorrentDownloadStation",
    "UsenetDownloadStation",
    "Flood",
    "TorrentFreeboxDownload",
    "Hadouken",
    "Nzbget",
    "NzbVortex",
    "Pneumatic",
    "QBittorrent",
    "RTorrent",
    "Sabnzbd",
    "TorrentBlackhole",
    "Transmission",
    "UsenetBlackhole",
    "UTorrent",
    "Vuze",
]

#: Import List schema implementations
PyarrImportListSchema = Literal[
    "AniListImport",
    "CustomImport",
    "ImdbListImport",
    "MyAnimeListImport",
    "PlexImport",
    "PlexRssImport",
    "SimklUserImport",
    "SonarrImport",
    "TraktListImport",
    "TraktPopularImport",
    "TraktUserImport",
]

#: Indexer schema implementations
PyarrIndexerSchema = Literal[
    "FileList",
    "HDBits",
    "IPTorrents",
    "Newznab",
    "Nyaa",
    "Omgwtfnzbs",
    "PassThePopcorn",
    "Rarbg",
    "TorrentRssIndexer",
    "TorrentPotato",
    "Torznab",
]

# --- Sonarr Literals ---

#: Sonarr commands
SonarrCommands = Literal[
    "Backup",
    "DownloadedEpisodesScan",
    "EpisodeSearch",
    "missingEpisodeSearch",
    "RefreshSeries",
    "RenameSeries",
    "RenameFiles",
    "RescanSeries",
    "RssSync",
    "SeasonSearch",
    "SeriesSearch",
]

#: Sonarr sort keys
SonarrSortKey = Literal[
    "airDateUtc",
    "date",
    "downloadClient",
    "episode",
    "episodeId",
    "episode.title",
    "id",
    "indexer",
    "language",
    "message",
    "path",
    "progress",
    "protocol",
    "quality",
    "ratings",
    "seriesId",
    "series.sortTitle",
    "size",
    "sourcetitle",
    "status",
    "timeleft",
]

# --- Radarr Literals ---

#: Radarr commands
RadarrCommands = Literal[
    "DownloadedMoviesScan",
    "MissingMoviesSearch",
    "MoviesSearch",
    "RefreshMovie",
    "RenameMovie",
    "RenameFiles",
    "Backup",
]

#: Radarr sort keys
RadarrSortKey = Literal[
    "date",
    "downloadClient",
    "id",
    "indexer",
    "languages",
    "message",
    "modieId",
    "movies.sortTitle",
    "path",
    "progress",
    "protocol",
    "quality",
    "ratings",
    "title",
    "size",
    "sourcetitle",
    "status",
    "timeleft",
]

#: Radarr event types
RadarrEventType = Literal[
    "unknown",
    "grabbed",
    "downloadFolderImported",
    "downloadFailed",
    "movieFileDeleted",
    "movieFolderImported",
    "movieFileRenamed",
    "downloadIgnored",
]

#: Radarr movie availability types
RadarrMonitorType = Literal["movieOnly", "movieAndCollections", "none"]

#: Radarr movie availability types
RadarrAvailabilityType = Literal["announced", "inCinemas", "released"]

# --- Lidarr Literals ---

#: Lidarr commands
LidarrCommand = Literal[
    "AlbumSearch",
    "ApplicationUpdateCheck",
    "ArtistSearch",
    "DownloadedAlbumsScan",
    "MissingAlbumSearch",
    "RefreshAlbum",
    "RefreshArtist",
]

#: Lidarr sort keys
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

#: Lidarr Import List schema implementations
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

# --- Readarr Literals ---

#: Readarr commands
ReadarrCommands = Literal[
    "ApplicationUpdateCheck",
    "AuthorSearch",
    "BookSearch",
    "RefreshAuthor",
    "RefreshBook",
    "RenameAuthor",
    "RenameFiles",
    "RescanFolders",
    "RssSync",
    "Backup",
    "MissingBookSearch",
]

#: Readarr sort keys
ReadarrSortKeys = Literal[
    "authorId",
    "Books.Id",
    "books.releaseDate",
    "downloadClient",
    "id",
    "indexer",
    "message",
    "path",
    "progress",
    "protocol",
    "quality",
    "ratings",
    "size",
    "sourcetitle",
    "status",
    "timeleft",
    "title",
]

#: Readarr search types
ReadarrSearchType = Literal["asin", "edition", "isbn", "author", "work"]

#: Readarr author monitor options
ReadarrAuthorMonitor = Literal["all", "future", "missing", "existing", "first", "latest", "none"]
