class PyarrError(Exception):
    """Generic PyArr Exception."""


class PyarrConnectionError(PyarrError):
    """Sonarr connection exception."""


class PyarrUnauthorizedError(PyarrError):
    """Unauthorised access exception"""


class PyarrAccessRestricted(PyarrError):
    """Pyarr access restricted exception."""


class PyarrResourceNotFound(PyarrError):
    """Pyarr resource not found exception"""


class PyarrBadGateway(PyarrError):
    """Pyarr bad gateway exception"""


class PyarrMissingProfile(PyarrError):
    """Pyarr missing profile"""


class PyarrMethodNotAllowed(PyarrError):
    """Pyarr method not allowed"""


class PyarrRecordNotFound(PyarrError):
    """Pyarr record was not found"""


class PyarrMissingArgument(PyarrError):
    """Missing one of multiple possible arguments"""


class PyarrBadRequest(PyarrError):
    """Bad Request, possible bug."""


class PyarrServerError(PyarrError):
    """Server Error, missing or incorrect options."""

    def __init__(self, message, response):
        super().__init__(message)
        self.response = response
