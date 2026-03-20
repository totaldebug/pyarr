from typing import Any

from pyarr.common.base import CommonActions
from pyarr.types import JsonArray


class Search(CommonActions):
    """Search actions for Prowlarr."""

    def get(self, query: str, indexer_ids: list[int] | None = None, **kwargs) -> JsonArray:
        """Perform a search across indexers.

        Args:
            query (str): Search query.
            indexer_ids (list[int] | None, optional): List of indexer IDs to search. Defaults to None.
            **kwargs: Additional search parameters.

        Returns:
            JsonArray: List of search results.
        """
        params: dict[str, Any] = {"query": query}
        if indexer_ids:
            params["indexerIds"] = indexer_ids
        if kwargs:
            params |= kwargs

        response = self.handler.request("search", params=params)
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'search' endpoint")
