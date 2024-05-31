from typing import Literal

#: Pyarr sort direction
PyarrSortDirection = Literal["ascending", "default", "descending"]


PyarrLogSortKey = Literal[
    "Id", "level", "time", "logger", "message", "exception", "exceptionType"
]
"""Log Sort Keys

Note:
    There may be more, but these are not well documented
    within Arr api docs.
"""


PyarrBlocklistSortKey = Literal["date"]
"""Block list sort keys

Note:
    There may be more, but these are not well documented
    within Arr api docs.
"""

PyarrHistorySortKey = Literal[
    "id",
    "date",
    "eventType",
    "series.title",
    "episode.title",
    "movieFile.relativePath",
    "sourceTitle",
    "status",
]
"""History sort keys

series.title (Sonarr)
episode.title (Sonarr)
status (Lidarr only)

Note:
    There may be more, but these are not well documented
    within Arr api docs.
"""

PyarrTaskSortKey = Literal["timeleft"]
"""Task sort keys

Note:
    There may be more, but these are not well documented
    within Arr api docs.
"""

PyarrLogFilterKey = Literal["level"]
"""Log filter keys

Note:
    There may be more, but these are not well documented
    within Arr api docs.
"""

PyarrLogFilterValue = Literal["all", "info", "warn", "error"]
"""Log filter values

Note:
    There may be more, but these are not well documented
    within Arr api docs.
"""


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
