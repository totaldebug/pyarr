from typing import Any, TypeVar

from pyarr.common.backup import Backup
from pyarr.common.blocklist import Blocklist
from pyarr.common.calendar import Calendar
from pyarr.common.command import Command
from pyarr.common.download_client import DownloadClient
from pyarr.common.history import History
from pyarr.common.import_list import ImportList
from pyarr.common.indexer import Indexer
from pyarr.common.log import Log
from pyarr.common.metadata import Metadata
from pyarr.common.notification import Notification
from pyarr.common.quality_definition import QualityDefinition
from pyarr.common.quality_profile import QualityProfile
from pyarr.common.queue import Queue
from pyarr.common.remote_path_mapping import RemotePathMapping
from pyarr.common.root_folder import RootFolder
from pyarr.common.system import System
from pyarr.common.tag import Tag
from pyarr.common.update import Update
from pyarr.utils.http import RequestHandler

T = TypeVar("T", bound="BaseArrClient")


class BaseArrClient:
    """Base class for all Arr clients."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int,
        tls: bool = True,
        base_path: str = "",
        request_timeout: int | None = None,
        api_ver: str | None = None,
    ):
        """Initializes the client with the provided host, API key, and optional parameters.

        Args:
            host (str): The host to connect to.
            api_key (str): The API key for authentication.
            port (int): The port to connect to.
            tls (bool, optional): Whether to use TLS. Defaults to True.
            base_path (str, optional): The base path for the API. Defaults to "".
            request_timeout (int | None, optional): The timeout for requests. Defaults to None.
            api_ver (str | None, optional): The API version to use. Defaults to None, automatically detected.
        """
        self.http_utils = RequestHandler(
            host,
            api_key,
            port=port,
            tls=tls,
            base_path=base_path,
            request_timeout=request_timeout,
            api_ver=api_ver,
        )
        self.history = History(self.http_utils)
        self.backup = Backup(self.http_utils)
        self.system = System(self.http_utils)
        self.tag = Tag(self.http_utils)
        self.blocklist = Blocklist(self.http_utils)
        self.calendar = Calendar(self.http_utils)
        self.root_folder = RootFolder(self.http_utils)
        self.update = Update(self.http_utils)
        self.metadata = Metadata(self.http_utils)
        self.log = Log(self.http_utils)
        self.indexer = Indexer(self.http_utils)
        self.download_client = DownloadClient(self.http_utils)
        self.import_list = ImportList(self.http_utils)
        self.notification = Notification(self.http_utils)
        self.quality_profile = QualityProfile(self.http_utils)
        self.quality_definition = QualityDefinition(self.http_utils)
        self.queue = Queue(self.http_utils)
        self.remote_path_mapping = RemotePathMapping(self.http_utils)
        self.command = Command(self.http_utils)

    def __enter__(self: T) -> T:
        """Enter the runtime context related to this object.

        Returns:
            T: The client instance.
        """
        # Initialize resources if needed
        self.http_utils.__enter__()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Exit the runtime context related to this object.

        Args:
            exc_type (Any): The exception type.
            exc_value (Any): The exception value.
            traceback (Any): The traceback.
        """
        # Clean up resources
        self.http_utils.__exit__(exc_type, exc_value, traceback)
