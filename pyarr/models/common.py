from enum import Enum

import enum_tools.documentation

enum_tools.documentation.INTERACTIVE = True


@enum_tools.documentation.document_enum
class PyarrSortDirection(str, Enum):
    """Pyarr sort direction"""

    ASC = "ascending"
    DEFAULT = "default"
    DESC = "descending"


@enum_tools.documentation.document_enum
class PyarrLogSortKey(str, Enum):
    """Log Sort Keys

    Note:
        There may be more, however these are yet to be identified
    """

    ID = "Id"
    LEVEL = "level"
    TIME = "time"
    LOGGER = "logger"
    MESSAGE = "message"
    EXCEPTION = "exception"
    EXCEPTION_TYPE = "exceptionType"


@enum_tools.documentation.document_enum
class PyarrBlocklistSortKey(str, Enum):
    """Block list sort keys"""

    DATE = "date"


@enum_tools.documentation.document_enum
class PyarrHistorySortKey(str, Enum):
    """history sort keys

    Note:
        There may be more, however these are yet to be identified
    """

    TIME = "time"


@enum_tools.documentation.document_enum
class PyarrTaskSortKey(str, Enum):
    """Task sort keys

    Note:
        There may be more, however these are yet to be identified
    """

    TIME_LEFT = "timeleft"


@enum_tools.documentation.document_enum
class PyarrLogFilterKey(str, Enum):
    """Log filter keys

    Note:
        There may be more, however these are yet to be identified
    """

    LEVEL = "level"


@enum_tools.documentation.document_enum
class PyarrLogFilterValue(str, Enum):
    """Log filter values

    Note:
        There may be more, however these are yet to be identified
    """

    ALL = "all"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


@enum_tools.documentation.document_enum
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


@enum_tools.documentation.document_enum
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


@enum_tools.documentation.document_enum
class PyarrImportListSchema(str, Enum):
    """Import List schema implementations"""

    PLEX = "PlexImport"
    SONARR = "SonarrImport"
    TRAKT_LIST = "TraktListImport"
    TRAKT_POPULAR = "TraktPopularImport"
    TRAKT_USER = "TraktUserImport"
