from dataclasses import dataclass
from enum import Enum


@dataclass(order=True)
class SonarrCommands(Enum):
    """Sonarr commands.

    Note:
        The parameters are supplied as `**kwargs` within the `post_command` method.
    """

    BACKUP = "Backup"
    """Backup of the Database"""
    DOWNLOADED_EPISODES_SCAN = "DownloadedEpisodesScan"
    """Scans downloaded episodes for state"""
    EPISODE_SEARCH = "EpisodeSearch"
    """Searches for all episondes, or specific ones in supplied list

    Args:
        episodeIds (lsit[int], optional): One or more episodeIds in a list
    """
    MISSING_EPISODE_SEARCH = "missingEpisodeSearch"
    """Searches for any missing episodes"""
    REFRESH_SERIES = "RefreshSeries"
    """Refreshes all series, if a `seriesId` is provided only that series will be refreshed

    Args:
        seriesId (int, optional): ID of specific series to be refreshed.
    """
    RENAME_SERIES = "RenameSeries"
    """Renames series to the expected naming format.

    Args:
        seriesIds (list[int]): List of Series IDs to rename.
    """

    RENAME_FILES = "RenameFiles"
    """Renames files to the expected naming format.

    Args:
        files (list[int]): List of File IDs to rename.
    """

    RESCAN_SERIES = "RescanSeries"
    """Re-scan all series, if `seriesId` is provided only that series will be Re-scanned.

    Args:
        seriesId (int, optional): ID of series to search for.
    """

    RSS_SYNC = "RssSync"
    """Synchronise RSS Feeds"""

    SEASON_SEARCH = "SeasonSearch"
    """Search for specific season.

    Args:
        seriesId (int): Series in which the season resides.
        seasonNumber (int): Season to search for.
    """

    SERIES_SEARCH = "SeriesSearch"
    """Searches for specific series.

    Args:
        seriesId (int): ID of series to search for.
    """


@dataclass(order=True)
class SonarrSortKey(Enum):
    """Sonarr sort keys."""

    AIR_DATE_UTC = "airDateUtc"
    DATE = "date"
    DOWNLOAD_CLIENT = "downloadClient"
    EPISODE = "episode"
    EPISODE_ID = "episodeId"
    EPISODE_TITLE = "episode.title"
    ID = "id"
    INDEXER = "indexer"
    LANGUAGE = "language"
    MESSAGE = "message"
    PATH = "path"
    PROGRESS = "progress"
    PROTOCOL = "protocol"
    QUALITY = "quality"
    RATINGS = "ratings"
    SERIES_ID = "seriesId"
    SERIES_TITLE = "series.sortTitle"
    SIZE = "size"
    SOURCE_TITLE = "sourcetitle"
    STATUS = "status"
    TIMELEFT = "timeleft"
