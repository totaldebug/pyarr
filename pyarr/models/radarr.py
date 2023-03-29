from enum import Enum


class RadarrCommands(str, Enum):
    """Radarr commands.

    Note:
        The parameters are supplied as `**kwargs` within the `post_command` method.
    """

    DOWNLOADED_MOVIES_SCAN = "DownloadedMoviesScan"
    """Scans for all clients for downloaded movies, or a single client by ID

    Args:
        clientid (int, optional): Download client ID
    """
    MISSING_MOVIES_SEARCH = "MissingMoviesSearch"
    """Searches for any missing movies"""
    REFRESH_MOVIE = "RefreshMovie"
    """Refreshes all of the movies, or specific by ID

    Args:
        movieid (int, Optional): ID of Movie
    """
    RENAME_MOVIE = "RenameMovie"
    """Rename specific movie to correct format.

    Args:
        movieid (list[int]): ID of Movie or movies
    """
    RESCAN_MOVIE = "RescanMovie"
    """Rescans specific movie

    Args:
        movieid (int): ID of Movie
    """
    RENAME_FILES = "RenameFiles"
    """Rename files to correct format

    Args:
        movieid (int): ID of Movie
    """
    BACKUP = "Backup"
    """Backup the server data"""


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


class RadarrMonitorType(str, Enum):
    """Radarr monitor types"""

    MOVIE_ONLY = "movieOnly"
    MOVIE_AND_COLLECTION = "movieAndCollection"
    NONE = "none"


class RadarrAvailabilityType(str, Enum):
    """Radarr availability types"""

    ANNOUNCED = "announced"
    IN_CINEMAS = "inCinemas"
    RELEASED = "released"
