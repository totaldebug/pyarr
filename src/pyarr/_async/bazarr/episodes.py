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
        if series_id is None and episode_id is None:
            raise PyarrMissingArgument("series_id or episode_id must be provided")

        params: dict[str, Any] = dict(kwargs)
        if series_id is not None:
            params["seriesid[]"] = series_id
        if episode_id is not None:
            params["episodeid[]"] = episode_id

        response = await self.handler.request("episodes", params=params)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'episodes' endpoint")

    async def download_subtitle(
        self,
        series_id: int,
        episode_id: int,
        language: str,
        forced: bool = False,
        hi: bool = False,
    ) -> JsonObject:
        """Searches for and downloads a subtitle for an episode.

        Args:
            series_id (int): The Sonarr series ID, sent as the ``seriesid`` parameter.
            episode_id (int): The Sonarr episode ID, sent as the ``episodeid`` parameter.
            language (str): Two letter language code.
            forced (bool, optional): Download a forced subtitle. Defaults to False.
            hi (bool, optional): Download a hearing impaired subtitle. Defaults to False.

        Returns:
            JsonObject: The response data.
        """
        params: dict[str, Any] = {
            "seriesid": series_id,
            "episodeid": episode_id,
            "language": language,
            "forced": forced,
            "hi": hi,
        }
        return await self.handler.request("episodes/subtitles", method="PATCH", params=params)

    async def delete_subtitle(
        self,
        series_id: int,
        episode_id: int,
        language: str,
        path: str,
        forced: bool = False,
        hi: bool = False,
    ) -> None:
        """Deletes a subtitle file from an episode.

        Args:
            series_id (int): The Sonarr series ID, sent as the ``seriesid`` parameter.
            episode_id (int): The Sonarr episode ID, sent as the ``episodeid`` parameter.
            language (str): Two letter language code.
            path (str): Path of the subtitle file to delete.
            forced (bool, optional): The subtitle is a forced subtitle. Defaults to False.
            hi (bool, optional): The subtitle is hearing impaired. Defaults to False.
        """
        params: dict[str, Any] = {
            "seriesid": series_id,
            "episodeid": episode_id,
            "language": language,
            "path": path,
            "forced": forced,
            "hi": hi,
        }
        await self.handler.request("episodes/subtitles", method="DELETE", params=params)
