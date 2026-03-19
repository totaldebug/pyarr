from pyarr.utils.http import RequestHandler


class Config:
    """Config actions for Lidarr."""

    def __init__(self, handler: RequestHandler):
        """Initializes the config actions with the provided request handler.

        Args:
            handler (RequestHandler): The request handler to use for API requests.
        """
        self.handler = handler
