from typing import Any

from pyarr._async.common.base import CommonActions
from pyarr.exceptions import PyarrMissingArgument
from pyarr.types import JsonObject


class Episodes(CommonActions):
    """Episode actions for Bazarr."""

    async def get(
        self,
        series_id: int | list[int] | None = None,
        episode_id: int | list[int] | None = None,
        **kwargs,
    ) -> JsonObject:
        """Returns the episodes Bazarr knows about for the given series or episodes.

        Bazarr requires at least one series or episode ID, it answers an unfiltered request with a 404.

        Args:
            series_id (int | list[int] | None, optional): One or more Sonarr series IDs to list episodes for.
                Sent as the ``seriesid[]`` parameter, repeated once per ID. Defaults to None.
            episode_id (int | list[int] | None, optional): One or more Sonarr episode IDs to list.
                Sent as the ``episodeid[]`` parameter, repeated once per ID. Defaults to None.
            **kwargs: Additional parameters to pass through to the endpoint.

        Returns:
            JsonObject: Dictionary with a ``data`` list of episodes.

        Raises:
            PyarrMissingArgument: If neither a series nor an episode ID is provided.
        """
        params: dict[str, Any] = dict(kwargs)
        if series_id is not None:
            params["seriesid[]"] = series_id
        if episode_id is not None:
            params["episodeid[]"] = episode_id

        if not params:
            raise PyarrMissingArgument("series_id or episode_id must be provided")

        response = await self.handler.request("episodes", params=params)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'episodes' endpoint")
