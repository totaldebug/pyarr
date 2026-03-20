from pyarr.client import BaseArrClient
from pyarr.radarr.config import Config
from pyarr.radarr.custom_filter import CustomFilter
from pyarr.radarr.manual_import import ManualImport
from pyarr.radarr.movie import Movie
from pyarr.radarr.movie_file import MovieFile
from pyarr.radarr.release import Release


class Whisparr(BaseArrClient):
    """Whisparr API client (Radarr fork)."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 6969,
        tls: bool = True,
        base_path: str = "",
        request_timeout: int | None = None,
        api_ver: str | None = None,
    ):
        """Initializes the Whisparr client.

        Args:
            host (str): The host to connect to.
            api_key (str): The API key for authentication.
            port (int, optional): The port to connect to. Defaults to 6969.
            tls (bool, optional): Whether to use TLS. Defaults to True.
            base_path (str, optional): The base path for the API. Defaults to "".
            request_timeout (int | None, optional): The timeout for requests. Defaults to None.
            api_ver (str | None, optional): The API version to use. Defaults to None.
        """
        super().__init__(
            host,
            api_key,
            port=port,
            tls=tls,
            base_path=base_path,
            request_timeout=request_timeout,
            api_ver=api_ver,
        )
        self.config = Config(self.http_utils)
        self.movie = Movie(self.http_utils)
        self.movie_file = MovieFile(self.http_utils)
        self.release = Release(self.http_utils)
        self.manual_import = ManualImport(self.http_utils)
        self.custom_filter = CustomFilter(self.http_utils)
