import httpx

from pyarr._async.bazarr.providers import Providers
from pyarr._async.bazarr.subtitles import Subtitles
from pyarr._async.client import BaseArrClient


class Bazarr(BaseArrClient):
    """Bazarr API client."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 6767,
        tls: bool = True,
        base_path: str = "",
        request_timeout: int | None = None,
        api_ver: str | None = "",
        session: httpx.AsyncClient | None = None,
        verify_ssl: bool = True,
        headers: dict[str, str] | None = None,
    ):
        """Initializes the Bazarr client.

        Args:
            host (str): The host to connect to.
            api_key (str): The API key for authentication.
            port (int, optional): The port to connect to. Defaults to 6767.
            tls (bool, optional): Whether to use TLS. Defaults to True.
            base_path (str, optional): The base path for the API. Defaults to "".
            request_timeout (int | None, optional): The timeout for requests. Defaults to None.
            api_ver (str | None, optional): The API version to use. Defaults to "" (Bazarr uses /api/).
            session (httpx.AsyncClient | None, optional): An existing httpx.AsyncClient session. Defaults to None.
            verify_ssl (bool, optional): Whether to verify SSL certificates. Defaults to True.
            headers (dict[str, str] | None, optional): Default headers to include in requests. Defaults to None.
        """
        super().__init__(
            host,
            api_key,
            port=port,
            tls=tls,
            base_path=base_path,
            request_timeout=request_timeout,
            api_ver=api_ver,
            session=session,
            verify_ssl=verify_ssl,
            headers=headers,
        )
        self.subtitles = Subtitles(self.http_utils)
        self.providers = Providers(self.http_utils)
