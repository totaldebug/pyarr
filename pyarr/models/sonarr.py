from typing import Literal

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
"""Sonarr commands.

Note:
    The parameters are supplied as `**kwargs` within the `post_command` method.

Backup:
    Backup of the Database

DownloadedEpisodesScan:
    Scans downloaded episodes for state

    Args:
        path (str): path to files

EpisodeSearch:
    Searches for all episondes, or specific ones in supplied list

    Args:
        episodeIds (lsit[int], optional): One or more episodeIds in a list

missingEpisodeSearch:
    Searches for any missing episodes

RefreshSeries:
    Refreshes all series, if a `seriesId` is provided only that series will be refreshed

    Args:
        seriesId (int, optional): ID of specific series to be refreshed.

RenameSeries:
    Renames series to the expected naming format.

    Args:
        seriesIds (list[int]): List of Series IDs to rename.

RenameFiles:
    Renames files to the expected naming format.

    Args:
        seriesId (int, optional): ID of series files relate to
        files (list[int]): List of File IDs to rename.

RescanSeries:
    Re-scan all series, if `seriesId` is provided only that series will be Re-scanned.

    Args:
        seriesId (int, optional): ID of series to search for.

RssSync:
    Synchronise RSS Feeds

SeasonSearch:
    Search for specific season.

    Args:
        seriesId (int): Series in which the season resides.
        seasonNumber (int): Season to search for.

SeriesSearch:
    Searches for specific series.

    Args:
        seriesId (int): ID of series to search for.
"""


#: Sonarr sort keys.
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
