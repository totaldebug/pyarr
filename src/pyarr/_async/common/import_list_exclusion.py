from pyarr._async.common.base import CommonActions
from pyarr._async.utils.http import RequestHandler
from pyarr.types import JsonArray, JsonObject


class ImportListExclusion(CommonActions):
    """Import list exclusion actions for Arr clients.

    The endpoint differs between applications: Radarr serves the exclusion list from
    ``exclusions``, while Sonarr, Lidarr, Readarr and Whisparr use ``importlistexclusion``.
    """

    def __init__(self, handler: RequestHandler, path: str = "importlistexclusion"):
        """Initializes the import list exclusion actions with the provided request handler.

        Args:
            handler (RequestHandler): The request handler to use for API requests.
            path (str, optional): The API endpoint path. Defaults to "importlistexclusion".
        """
        super().__init__(handler)
        self.path = path

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of import list exclusions or a specific exclusion by ID.

        Args:
            item_id (int | None, optional): ID of the exclusion to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get(self.path, item_id=item_id)

    async def add(self, data: JsonObject) -> JsonObject:
        """Add an import list exclusion.

        The payload is application specific, for example Radarr expects ``tmdbId``,
        ``movieTitle`` and ``movieYear``, Sonarr and Whisparr expect ``tvdbId``, ``title``
        and ``year``, Lidarr expects ``foreignId`` and ``artistName``, and Readarr expects
        ``foreignId`` and ``authorName``.

        Args:
            data (JsonObject): Dictionary containing the exclusion to add.

        Returns:
            JsonObject: Dictionary of the added exclusion.
        """
        response = await self.handler.request(self.path, method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the '{self.path}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete an import list exclusion by ID.

        Args:
            item_id (int): The ID of the exclusion to delete.
        """
        await self._delete(self.path, item_id=item_id)
