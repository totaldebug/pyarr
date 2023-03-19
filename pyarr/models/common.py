from enum import Enum


class PyarrSortDirection(str, Enum):
    """Pyarr sort direction"""

    ASC = "ascending"
    DEFAULT = "default"
    DESC = "descending"


class PyarrLogSortKey(str, Enum):
    """Log Sort Keys

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    ID = "Id"
    LEVEL = "level"
    TIME = "time"
    LOGGER = "logger"
    MESSAGE = "message"
    EXCEPTION = "exception"
    EXCEPTION_TYPE = "exceptionType"


class PyarrBlocklistSortKey(str, Enum):
    """Block list sort keys

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    DATE = "date"


class PyarrHistorySortKey(str, Enum):
    """History sort keys

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    TIME = "time"


class PyarrTaskSortKey(str, Enum):
    """Task sort keys

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    TIME_LEFT = "timeleft"


class PyarrLogFilterKey(str, Enum):
    """Log filter keys

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    LEVEL = "level"


class PyarrLogFilterValue(str, Enum):
    """Log filter values

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    ALL = "all"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


class PyarrNotificationSchema(str, Enum):
    """Notification schema implementations"""

    BOXCAR = "Boxcar"
    CUSTOM = "CustomScript"
    DISCORD = "Discord"
    EMAIL = "Email"
    MEDIA_BROWSER = "MediaBrowser"
    GOTIFY = "Gotify"
    JOIN = "Join"
    XBMC = "Xbmc"
    MAILGUN = "MailGun"
    PLEX_THEATER = "PlexHomeTheater"
    PLEX_CLIENT = "PlexClient"
    PLEX_SERVER = "PlexServer"
    PROWL = "Prowl"
    PUSH_BULLET = "PushBullet"
    PUSHOVER = "Pushover"
    SAND_GRID = "SendGrid"
    SLACK = "Slack"
    SYNOLOGY_INDEXER = "SynologyIndexer"
    TELEGRAM = "Telegram"
    TRAKT = "Trakt"
    TWITTER = "Twitter"
    WEBHOOK = "Webhook"


class PyarrDownloadClientSchema(str, Enum):
    """Download client schema implementations"""

    ARIA2 = "Aria2"
    DELUGE = "Deluge"
    TORRENT_DOWNLOAD_STATION = "TorrentDownloadStation"
    USENET_DOWNLOAD_STATION = "UsenetDownloadStation"
    FLOOD = "Flood"
    HADOUKEN = "Hadouken"
    NZB_GET = "Nzbget"
    NZB_VORTEX = "NzbVortex"
    PNEUMATIC = "Pneumatic"
    Q_BITTORRENT = "QBittorrent"
    R_TORRENT = "RTorrent"
    SABNZBD = "Sabnzbd"
    TORRENT_BLACKHOLE = "TorrentBlackhole"
    TRANSMISSION = "Transmission"
    USENET_BLACKHOLE = "UsenetBlackhole"
    U_TORRENT = "UTorrent"
    VUZE = "Vuze"


class PyarrImportListSchema(str, Enum):
    """Import List schema implementations"""

    PLEX = "PlexImport"
    SONARR = "SonarrImport"
    TRAKT_LIST = "TraktListImport"
    TRAKT_POPULAR = "TraktPopularImport"
    TRAKT_USER = "TraktUserImport"


class PyarrIndexerSchema(str, Enum):
    """Import List schema implementations"""

    FILE_LIST = "FileList"
    HD_BITS = "HDBits"
    IP_TORRENTS = "IPTorrents"
    NEWZNAB = "Newznab"
    NYAA = "Nyaa"
    OMGWTFNZBS = "Omgwtfnzbs"
    PASS_THE_POPCORN = "PassThePopcorn"
    RARBG = "Rarbg"
    TORRENT_RSS_INDEXER = "TorrentRssIndexer"
    TORRENT_POTATO = "TorrentPotato"
    TORZNAB = "Torznab"
