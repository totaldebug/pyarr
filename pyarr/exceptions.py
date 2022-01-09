class PyarrError(Exception):
    """Generic PyArr Exception."""

    pass


class PyarrConnectionError(PyarrError):
    """Sonarr connection exception."""

    pass


class PyarrUnauthorizedError(PyarrError):
    """Unauthorised access exception"""

    pass


class PyarrAccessRestricted(PyarrError):
    """Pyarr access restricted exception."""

    pass


class PyarrResourceNotFound(PyarrError):
    """Pyarr resource not found exception"""

    pass


class PyarrBadGateway(PyarrError):
    """Pyarr bad gateway exception"""

    pass


class PyarrMissingProfile(PyarrError):
    """Pyarr missing profile"""

    pass
