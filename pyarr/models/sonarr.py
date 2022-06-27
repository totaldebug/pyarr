from enum import Enum


class SonarrCommands(str, Enum):
    """Sonarr commands."""

    DOWNLOADED_EPISODES_SCAN = "DownloadedEpisodesScan"
    EPISODE_SEARCH = "EpisodeSearch"
    REFRESH_SERIES = "RefreshSeries"
    RENAME_SERIES = "RenameSeries"
    RESCAN_SERIES = "RescanSeries"
    SEASON_SEARCH = "SeasonSearch"
    SERIES_SEARCH = "SeriesSearch"


class SonarrSortKeys(str, Enum):
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
