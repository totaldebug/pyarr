from typing import Literal

RadarrCommands = Literal[
    "DownloadedMoviesScan",
    "MissingMoviesSearch",
    "MoviesSearch",
    "RefreshMovie",
    "RenameMovie",
    "RenameFiles",
    "Backup",
]
"""
Radarr commands.

    Note:
        The parameters are supplied as `**kwargs` within the `post_command` method.

DownloadedMoviesScan:
    Scans downloaded episodes for state

    Args:
        path (str): path to files

MissingMoviesSearch:
    Searches for any missing movies

MoviesSearch:
    Searches for the specified movie or movies

    Args:
        movieIds (list[int]): ID of Movie or movies

RefreshMovie:
    Refreshes all of the movies, or specific by ID

    Args:
        movieId (int, Optional): ID of Movie

RenameMovie:
    Rename specific movie to correct format.

    Args:
        movieId (int): ID of Movie or movies
        movieIds (list[int]): ID of Movie or movies

RescanMovie:
    Rescans specific movie

    Args:
        movieId (int): ID of Movie

RenameFiles:
    Rename files to correct format

    Args:
        movieId (int): ID of Movie
        files (int): ID of files

RssSync:
    Synchronise RSS Feeds

Backup:
    Backup the server data
"""

#: Radarr sort keys
RadarrSortKey = Literal[
    "date",
    "downloadClient",
    "id",
    "indexer",
    "languages",
    "message",
    "modieId",
    "movies.sortTitle",
    "path",
    "progress",
    "protocol",
    "quality",
    "ratings",
    "title",
    "size",
    "sourcetitle",
    "status",
    "timeleft",
]


#: Radarr event types
RadarrEventType = Literal[
    "unknown",
    "grabbed",
    "downloadFolderImported",
    "downloadFailed",
    "movieFileDeleted",
    "movieFolderImported",
    "movieFileRenamed",
    "downloadIgnored",
]

#: Radarr movie availability types
RadarrMonitorType = Literal["movieOnly", "movieAndCollections", "none"]

#: Radarr movie availability types
RadarrAvailabilityType = Literal["announced", "inCinemas", "released"]
