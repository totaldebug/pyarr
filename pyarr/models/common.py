from dataclasses import dataclass
from enum import Enum


@dataclass(order=True)
class PyarrSortDirection(Enum):
    """Pyarr sort direction"""

    ASC = "ascending"
    DEFAULT = "default"
    DESC = "descending"


@dataclass(order=True)
class PyarrLogSortKey(Enum):
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


@dataclass(order=True)
class PyarrBlocklistSortKey(Enum):
    """Block list sort keys

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    DATE = "date"


@dataclass(order=True)
class PyarrHistorySortKey(Enum):
    """History sort keys

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    TIME = "time"


@dataclass(order=True)
class PyarrTaskSortKey(Enum):
    """Task sort keys

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    TIME_LEFT = "timeleft"


@dataclass(order=True)
class PyarrLogFilterKey(Enum):
    """Log filter keys

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    LEVEL = "level"


@dataclass(order=True)
class PyarrLogFilterValue(Enum):
    """Log filter values

    Note:
        There may be more, but these are not well documented
        within Arr api docs.
    """

    ALL = "all"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


@dataclass(order=True)
class PyarrNotificationSchema(Enum):
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


@dataclass(order=True)
class PyarrDownloadClientSchema(Enum):
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


@dataclass(order=True)
class PyarrImportListSchema(Enum):
    """Import List schema implementations"""

    PLEX = "PlexImport"
    SONARR = "SonarrImport"
    TRAKT_LIST = "TraktListImport"
    TRAKT_POPULAR = "TraktPopularImport"
    TRAKT_USER = "TraktUserImport"
