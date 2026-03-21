from pyarr._async.common.base import CommonActions
from pyarr.exceptions import PyarrMissingArgument
from pyarr.types import JsonObject


class Log(CommonActions):
    """Log actions for Arr clients."""

    async def get(
        self,
        page: int | None = None,
        page_size: int | None = None,
        sort_key: str | None = None,
        sort_dir: str | None = None,
        filter_key: str | None = None,
        filter_value: str | None = None,
    ) -> JsonObject:
        """Gets logs from instance.

        Args:
            page (int | None, optional): Specify page to return. Defaults to None.
            page_size (int | None, optional): Number of items per page. Defaults to None.
            sort_key (str | None, optional): Field to sort by. Defaults to None.
            sort_dir (str | None, optional): Direction to sort. Defaults to None.
            filter_key (str | None, optional): Key to filter by. Defaults to None.
            filter_value (str | None, optional): Value of the filter. Defaults to None.

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

        if filter_key and filter_value:
            params["filterKey"] = filter_key
            params["filterValue"] = filter_value
        elif filter_key or filter_value:
            raise PyarrMissingArgument("filter_key and filter_value must be used together")

        response = await self.handler.request("log", params=params)
        if isinstance(response, dict):
            return response
        raise TypeError("Expected response to be a dictionary")
