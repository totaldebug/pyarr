from enum import Enum

import enum_tools.documentation

enum_tools.documentation.INTERACTIVE = True


@enum_tools.documentation.document_enum
class SonarrCommands(str, Enum):
    """Sonarr commands."""

    BACKUP = "Backup"
    """No parameters required"""
    DOWNLOADED_EPISODES_SCAN = "DownloadedEpisodesScan"
    """No parameters required"""
    EPISODE_SEARCH = "EpisodeSearch"
    """episodeIds (lsit[int], optional) - One or more episodeIds in a list"""
    MISSING_EPISODE_SEARCH = "missingEpisodeSearch"
    """No parameters required"""
    REFRESH_SERIES = "RefreshSeries"
    """
    seriesId (int, optional) - If not set, all series will be refreshed and scanned
    """
    RENAME_SERIES = "RenameSeries"
    """seriesIds (list[int]) - List of Series IDs to rename"""
    RENAME_FILES = "RenameFiles"
    """files (list[int]) - List of File IDs to rename"""
    RESCAN_SERIES = "RescanSeries"
    """seriesId (int, optional) - If not set all series will be scanned"""
    RSS_SYNC = "RssSync"
    """No parameters required"""
    SEASON_SEARCH = "SeasonSearch"
    """seriesId (int), seasonNumber (int) both are required"""
    SERIES_SEARCH = "SeriesSearch"
    """seriesId (int) required"""


@enum_tools.documentation.document_enum
class SonarrSortKey(str, Enum):
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
