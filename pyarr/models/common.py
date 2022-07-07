from enum import Enum


class PyarrSortDirection(str, Enum):
    """Pyarr sort direction"""

    ASC = "ascending"
    DEFAULT = "default"
    DESC = "descending"


class PyarrLogSortKey(str, Enum):
    """Log Sort Keys

    Note:
        There may be more, however these are yet to be identified
    """

    ID = "Id"
    LEVEL = "level"
    TIME = "time"
    LOGGER = "logger"
    MESSAGE = "message"
    EXCEPTION = "exception"
    EXCEPTION_TYPE = "exceptionType"


class PyarrBlocklistSortKey(str, Enum):
    """Block list sort keys"""

    DATE = "date"


class PyarrHistorySortKey(str, Enum):
    """history sort keys

    Note:
        There may be more, however these are yet to be identified
    """

    TIME = "time"


class PyarrLogFilterKey(str, Enum):
    """Log filter keys

    Note:
        There may be more, however these are yet to be identified
    """

    LEVEL = "level"


class PyarrLogFilterValue(str, Enum):
    """Log filter values

    Note:
        There may be more, however these are yet to be identified
    """

    ALL = "all"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
