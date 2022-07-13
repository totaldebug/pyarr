from enum import Enum

import enum_tools.documentation

enum_tools.documentation.INTERACTIVE = True


@enum_tools.documentation.document_enum
class ReadarrCommands(str, Enum):
    """Readarr commands."""

    APP_UPDATE_CHECK = "ApplicationUpdateCheck"
    AUTHOR_SEARCH = "AuthorSearch"
    BOOK_SEARCH = "BookSearch"
    REFRESH_AUTHOR = "RefreshAuthor"
    REFRESH_BOOK = "RefreshBook"
    RENAME_AUTHOR = "RenameAuthor"
    RESCAN_FOLDERS = "RescanFolders"


@enum_tools.documentation.document_enum
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


@enum_tools.documentation.document_enum
class ReadarrBookTypes(str, Enum):
    """Readarr book types."""

    ASIN = "asin"
    GOODREADS = "goodreads"
    ISBN = "isbn"


@enum_tools.documentation.document_enum
class ReadarrAuthorMonitor(str, Enum):
    """Readarr author monitor options."""

    ALL = "all"
    FUTURE = "future"
    MISSING = "missing"
    EXISTING = "existing"
    FIRST_BOOK = "first"
    LATEST_BOOK = "latest"
    NONE = "none"
