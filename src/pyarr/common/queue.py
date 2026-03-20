from pyarr.common.base import CommonActions
from pyarr.exceptions import PyarrMissingArgument
from pyarr.types import JsonObject


class Queue(CommonActions):
    """Queue actions for Arr clients."""

    def get(
        self,
        page: int | None = None,
        page_size: int | None = None,
        sort_key: str | None = None,
        sort_dir: str | None = None,
        **kwargs,
    ) -> JsonObject:
        """Returns the list of items in the queue.

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

        response = self.handler.request("queue", params=params)
        if isinstance(response, dict):
            return response
        raise TypeError("Expected response to be a dictionary")

    def delete(
        self,
        item_id: int,
        remove_from_client: bool | None = None,
        blocklist: bool | None = None,
        skip_redundant_dictionary_check: bool | None = None,
        mark_as_failed: bool | None = None,
        message: str | None = None,
    ) -> None:
        """Remove an item from the queue.

        Args:
            item_id (int): ID of the item to be removed.
            remove_from_client (bool | None, optional): Remove the item from the client. Defaults to None.
            blocklist (bool | None, optional): Add the item to the blocklist. Defaults to None.
            skip_redundant_dictionary_check (bool | None, optional): Skip redundant dictionary check. Defaults to None.
            mark_as_failed (bool | None, optional): Mark the item as failed (Sonarr v5). Defaults to None.
            message (str | None, optional): Message for failure (Sonarr v5). Defaults to None.
        """
        params: dict[str, bool | str] = {}
        if remove_from_client is not None:
            params["removeFromClient"] = remove_from_client
        if blocklist is not None:
            params["blocklist"] = blocklist
        if skip_redundant_dictionary_check is not None:
            params["skipRedundantDictionaryCheck"] = skip_redundant_dictionary_check
        if mark_as_failed is not None:
            params["markAsFailed"] = mark_as_failed
        if message is not None:
            params["message"] = message

        self.handler.request(f"queue/{item_id}", method="DELETE", params=params)

    def bulk_delete(
        self,
        item_ids: list[int],
        remove_from_client: bool | None = None,
        blocklist: bool | None = None,
    ) -> None:
        """Remove multiple items from the queue.

        Args:
            item_ids (list[int]): List of IDs to be removed.
            remove_from_client (bool | None, optional): Remove the items from the client. Defaults to None.
            blocklist (bool | None, optional): Add the items to the blocklist. Defaults to None.
        """
        params: dict[str, bool] = {}
        if remove_from_client is not None:
            params["removeFromClient"] = remove_from_client
        if blocklist is not None:
            params["blocklist"] = blocklist

        json_data = {"ids": item_ids}
        self.handler.request("queue/bulk", method="DELETE", params=params, json_data=json_data)
