from enum import Enum

import enum_tools.documentation

enum_tools.documentation.INTERACTIVE = True


@enum_tools.documentation.document_enum
class RadarrCommands(str, Enum):
    """Radarr commands."""

    DOWNLOADED_MOVIES_SCAN = "DownloadedMoviesScan"
    MISSING_MOVIES_SEARCH = "MissingMoviesSearch"
    REFRESH_MOVIE = "RefreshMovie"
    RENAME_MOVIE = "RenameMovie"
    RESCAN_MOVIE = "RescanMovie"
    RENAME_FILES = "RenameFiles"
    BACKUP = "Backup"


@enum_tools.documentation.document_enum
class RadarrSortKeys(str, Enum):
    """Radarr sort keys."""

    DATE = "date"
    DOWNLOAD_CLIENT = "downloadClient"
    ID = "id"
    INDEXER = "indexer"
    LANGUAGES = "languages"
    MESSAGE = "message"
    MOVIE_ID = "modieId"
    MOVIE_TITLE = "movies.sortTitle"
    PATH = "path"
    PROGRESS = "progress"
    PROTOCOL = "protocol"
    QUALITY = "quality"
    RATINGS = "ratings"
    RELEASE_TITLE = "title"
    SIZE = "size"
    SOURCE_TITLE = "sourcetitle"
    STATUS = "status"
    TIMELEFT = "timeleft"


@enum_tools.documentation.document_enum
class RadarrEventType(str, Enum):
    """Radarr event types"""

    UNKNOWN = "unknown"
    GRABBED = "grabbed"
    DOWNLOAD_FILDER_INPORTED = "downloadFolderImported"
    DOWNLOAD_FAILED = "downloadFailed"
    MOVIE_FILE_DELETED = "movieFileDeleted"
    MOVIE_FOLDER_IMPORTED = "movieFolderImported"
    MOVIE_FILE_RENAMED = "movieFileRenamed"
    DOWNLOAD_IGNORED = "downloadIgnored"
