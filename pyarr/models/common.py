from enum import Enum

import enum_tools.documentation

enum_tools.documentation.INTERACTIVE = True


@enum_tools.documentation.document_enum
class PyarrSortDirection(str, Enum):
    """Pyarr sort direction"""

    ASC = "ascending"
    DEFAULT = "default"
    DESC = "descending"


@enum_tools.documentation.document_enum
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


@enum_tools.documentation.document_enum
class PyarrBlocklistSortKey(str, Enum):
    """Block list sort keys"""

    DATE = "date"


@enum_tools.documentation.document_enum
class PyarrHistorySortKey(str, Enum):
    """history sort keys

    Note:
        There may be more, however these are yet to be identified
    """

    TIME = "time"


@enum_tools.documentation.document_enum
class PyarrTaskSortKey(str, Enum):
    """Task sort keys

    Note:
        There may be more, however these are yet to be identified
    """

    TIME_LEFT = "timeleft"


@enum_tools.documentation.document_enum
class PyarrLogFilterKey(str, Enum):
    """Log filter keys

    Note:
        There may be more, however these are yet to be identified
    """

    LEVEL = "level"


@enum_tools.documentation.document_enum
class PyarrLogFilterValue(str, Enum):
    """Log filter values

    Note:
        There may be more, however these are yet to be identified
    """

    ALL = "all"
    INFO = "info"
    WARN = "warn"
    ERROR = "error"
