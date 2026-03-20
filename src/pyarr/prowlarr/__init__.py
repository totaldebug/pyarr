from pyarr.client import BaseArrClient
from pyarr.common.indexer import Indexer
from pyarr.prowlarr.applications import Applications
from pyarr.prowlarr.indexer_proxy import IndexerProxy
from pyarr.prowlarr.search import Search


class Prowlarr(BaseArrClient):
    """Prowlarr API client."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 9696,
        tls: bool = True,
        base_path: str = "",
        request_timeout: int | None = None,
        api_ver: str | None = "v1",
    ):
        """Initializes the Prowlarr client.

        Args:
            host (str): The host to connect to.
            api_key (str): The API key for authentication.
            port (int, optional): The port to connect to. Defaults to 9696.
            tls (bool, optional): Whether to use TLS. Defaults to True.
            base_path (str, optional): The base path for the API. Defaults to "".
            request_timeout (int | None, optional): The timeout for requests. Defaults to None.
            api_ver (str | None, optional): The API version to use. Defaults to "v1".
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
        self.indexer = Indexer(self.http_utils)
        self.search = Search(self.http_utils)
        self.applications = Applications(self.http_utils)
        self.indexer_proxy = IndexerProxy(self.http_utils)
