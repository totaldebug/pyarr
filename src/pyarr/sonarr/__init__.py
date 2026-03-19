from pyarr.client import BaseArrClient
from pyarr.sonarr.config import Config
from pyarr.sonarr.episode import Episode
from pyarr.sonarr.episode_file import EpisodeFile
from pyarr.sonarr.manual_import import ManualImport
from pyarr.sonarr.release import Release
from pyarr.sonarr.series import Series


class Sonarr(BaseArrClient):
    """Sonarr API client."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 8989,
        tls: bool = True,
        base_path: str = "",
        request_timeout: int | None = None,
        api_ver: str | None = None,
    ):
        """Initializes the Sonarr client with the provided host, API key, and optional parameters.

        Args:
            host (str): The host to connect to.
            api_key (str): The API key for authentication.
            port (int, optional): The port to connect to. Defaults to 8989.
            tls (bool, optional): Whether to use TLS. Defaults to True.
            base_path (str, optional): The base path for the API. Defaults to "".
            request_timeout (int | None, optional): The timeout for requests. Defaults to None.
            api_ver (str | None, optional): The API version to use. Defaults to None, automatically detected.
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
        self.series = Series(self.http_utils)
        self.episode = Episode(self.http_utils)
        self.episode_file = EpisodeFile(self.http_utils)
        self.release = Release(self.http_utils)
        self.manual_import = ManualImport(self.http_utils)
