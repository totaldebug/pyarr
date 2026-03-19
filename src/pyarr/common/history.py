from pyarr.common.base import CommonActions
from pyarr.exceptions import PyarrMissingArgument
from pyarr.literals import PyarrHistorySortKey, PyarrSortDirection
from pyarr.types import JsonObject


class History(CommonActions):
    """History actions for Arr clients."""

    def get(
        self,
        page: int | None = None,
        page_size: int | None = None,
        sort_key: PyarrHistorySortKey | None = None,
        sort_dir: PyarrSortDirection | None = None,
    ) -> JsonObject:
        """Gets history (grabs/failures/completed).

        Args:
            page (int | None, optional): Page number to return. Defaults to None.
            page_size (int | None, optional): Number of items per page. Defaults to None.
            sort_key (PyarrHistorySortKey | None, optional): Field to sort by. Defaults to None.
            sort_dir (PyarrSortDirection | None, optional): Direction to sort the items. Defaults to None.

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

        response = self.handler.request("history", params=params)

        if isinstance(response, dict):
            return response
        raise TypeError("Expected response to be a dictionary")
