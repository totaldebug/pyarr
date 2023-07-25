from typing import Literal

ReadarrCommands = Literal[
    "ApplicationUpdateCheck",
    "AuthorSearch",
    "BookSearch",
    "RefreshAuthor",
    "RefreshBook",
    "RenameAuthor",
    "RenameFiles",
    "RescanFolders",
    "RssSync",
    "Backup",
    "MissingBookSearch",
]
"""Readarr commands.

Note:
    The parameters are supplied as `**kwargs` within the `post_command` method.

ApplicationUpdateCheck:
    Checks for Application updates

AuthorSearch:
    Search for specific author by ID

    Args:
        authorId (int): ID for Author

BookSearch:
    Search for specific Book by ID

    Args:
        bookId (int): ID for Book

RefreshAuthor:
    Refresh all Authors, or by specific ID

    Args:
        authorId (int, optional): ID for Author

RefreshBook:
    Refresh all Books, or by specific ID

    Args:
        bookId (int, optional): ID for Book

RenameAuthor:
    Rename all Authors, or by list of Ids

    Args:
        authorIds (list[int], optional): IDs for Authors

RenameFiles:
    Rename all files, or by specific ID

    Args:
        authorId (int, optional): ID for Author
        files (str): ID of files

RescanFolders:
    Rescans folders

RssSync:
    Synchronise RSS Feeds

Backup:
    Backup of the Database

MissingBookSearch:
    Searches for any missing books
"""

#: Readarr sort keys.
ReadarrSortKeys = Literal[
    "authorId",
    "Books.Id",
    "books.releaseDate",
    "downloadClient",
    "id",
    "indexer",
    "message",
    "path",
    "progress",
    "protocol",
    "quality",
    "ratings",
    "size",
    "sourcetitle",
    "status",
    "timeleft",
    "title",
]


#: Readarr search types.
ReadarrSearchType = Literal["asin", "edition", "isbn", "author", "work"]


#: Readarr author monitor options.
ReadarrAuthorMonitor = Literal[
    "all", "future", "missing", "existing", "first", "latest", "none"
]
