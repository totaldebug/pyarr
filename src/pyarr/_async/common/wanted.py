from pyarr._async.common.base import CommonActions
from pyarr._async.utils.http import RequestHandler
from pyarr.exceptions import PyarrMissingArgument
from pyarr.types import JsonObject


class Wanted(CommonActions):
    """Wanted actions for Arr clients."""

    def __init__(self, handler: RequestHandler, path: str = "wanted/missing"):
        """Initializes the wanted actions with the provided request handler.

        Args:
            handler (RequestHandler): The request handler to use for API requests.
            path (str, optional): The API endpoint path. Defaults to "wanted/missing".
        """
        super().__init__(handler)
        self.path = path

    async def get(
        self,
        page: int | None = None,
        page_size: int | None = None,
        sort_key: str | None = None,
        sort_dir: str | None = None,
        **kwargs,
    ) -> JsonObject:
        """Gets wanted/missing items.

        Args:
            page (int | None, optional): Page number to return. Defaults to None.
            page_size (int | None, optional): Number of items per page. Defaults to None.
            sort_key (str | None, optional): Field to sort by. Defaults to None.
            sort_dir (str | None, optional): Direction to sort the items. Defaults to None.
            **kwargs: Additional parameters for specific clients.

        Returns:
           JsonObject: Dictionary with items.
        """
        params: dict[str, str | int] = {}

        if page:
            params["page"] = page

        if page_size:
            params["pageSize"] = page_size

        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir must be used together")

        if kwargs:
            params |= kwargs

        response = await self.handler.request(self.path, params=params)

        if isinstance(response, dict):
            return response
        raise TypeError("Expected response to be a dictionary")
