from enum import Enum


class ReadarrCommands(str, Enum):
    """Readarr commands.

    Note:
        The parameters are supplied as `**kwargs` within the `post_command` method.
    """

    APP_UPDATE_CHECK: str = "ApplicationUpdateCheck"
    """Checks for Application updates"""
    AUTHOR_SEARCH = "AuthorSearch"
    """Search for specific author by ID

    Args:
        authorId (int): ID for Author
    """
    BOOK_SEARCH = "BookSearch"
    """Search for specific Book by ID

    Args:
        bookId (int): ID for Book
    """
    REFRESH_AUTHOR = "RefreshAuthor"
    """Refresh all Authors, or by specific ID

    Args:
        authorId (int, optional): ID for Author
    """
    REFRESH_BOOK = "RefreshBook"
    """Refresh all Books, or by specific ID

    Args:
        bookId (int, optional): ID for Book
    """
    RENAME_AUTHOR = "RenameAuthor"
    """Rename all Authors, or by list of Ids

    Args:
        authorIds (list[int], optional): IDs for Authors
    """
    RENAME_FILES = "RenameFiles"
    """Rename all files, or by specific ID

    Args:
        authorId (int, optional): ID for Author
    """
    RESCAN_FOLDERS = "RescanFolders"
    """Rescans folders"""
    RSS_SYNC = "RssSync"
    """Synchronise RSS Feeds"""
    BACKUP = "Backup"
    """Backup of the Database"""
    MISSING_BOOK_SEARCH = "MissingBookSearch"
    """Searches for any missing books"""


class ReadarrSortKeys(str, Enum):
    """Readarr sort keys."""

    AUTHOR_ID = "authorId"
    BOOK_ID = "Books.Id"
    DATE = "books.releaseDate"
    DOWNLOAD_CLIENT = "downloadClient"
    ID = "id"
    INDEXER = "indexer"
    MESSAGE = "message"
    PATH = "path"
    PROGRESS = "progress"
    PROTOCOL = "protocol"
    QUALITY = "quality"
    RATINGS = "ratings"
    SIZE = "size"
    SOURCE_TITLE = "sourcetitle"
    STATUS = "status"
    TIMELEFT = "timeleft"
    TITLE = "title"


class ReadarrBookTypes(str, Enum):
    """Readarr book types."""

    ASIN = "asin"
    GOODREADS = "goodreads"
    ISBN = "isbn"


class ReadarrAuthorMonitor(str, Enum):
    """Readarr author monitor options."""

    ALL: str = "all"
    FUTURE = "future"
    MISSING = "missing"
    EXISTING = "existing"
    FIRST_BOOK = "first"
    LATEST_BOOK = "latest"
    NONE = "none"
