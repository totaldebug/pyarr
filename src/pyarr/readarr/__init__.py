from pyarr.client import BaseArrClient
from pyarr.readarr.author import Author
from pyarr.readarr.book import Book
from pyarr.readarr.config import Config
from pyarr.readarr.delay_profile import DelayProfile
from pyarr.readarr.edition import Edition
from pyarr.readarr.manual_import import ManualImport
from pyarr.readarr.metadata_profile import MetadataProfile
from pyarr.readarr.release_profile import ReleaseProfile


class Readarr(BaseArrClient):
    """Readarr API client."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 8787,
        tls: bool = True,
        base_path: str = "",
        request_timeout: int | None = None,
        api_ver: str | None = None,
    ):
        """Initializes the Readarr client with the provided host, API key, and optional parameters.

        Args:
            host (str): The host to connect to.
            api_key (str): The API key for authentication.
            port (int, optional): The port to connect to. Defaults to 8787.
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
        self.author = Author(self.http_utils)
        self.book = Book(self.http_utils)
        self.edition = Edition(self.http_utils)
        self.metadata_profile = MetadataProfile(self.http_utils)
        self.release_profile = ReleaseProfile(self.http_utils)
        self.delay_profile = DelayProfile(self.http_utils)
        self.manual_import = ManualImport(self.http_utils)
