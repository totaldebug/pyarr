from typing import Any

from pyarr._async.common.base import CommonActions
from pyarr.exceptions import PyarrMissingArgument
from pyarr.literals import BazarrActions
from pyarr.types import JsonObject


class Series(CommonActions):
    """Series actions for Bazarr."""

    async def get(self, series_id: int | list[int] | None = None, **kwargs) -> JsonObject:
        """Returns the series Bazarr knows about.

        Args:
            series_id (int | list[int] | None, optional): Limit the results to one or more Sonarr series IDs.
                Sent as the ``seriesid[]`` parameter, repeated once per ID. Defaults to None (all series).
            **kwargs: Additional parameters, such as ``start`` and ``length`` for paging.

        Returns:
            JsonObject: Dictionary with a ``data`` list of series and a ``total`` count.
        """
        params: dict[str, Any] = dict(kwargs)
        if series_id is not None:
            params["seriesid[]"] = series_id

        response = await self.handler.request("series", params=params)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'series' endpoint")

    async def run_action(self, action: BazarrActions, series_id: int | None = None) -> None:
        """Runs an action against a series, which is how Bazarr is asked to do work.

        Bazarr answers a successful action with a 204 and no body, so there is nothing to return.

        Args:
            action (BazarrActions): The action to run. One of ``scan-disk``, ``search-missing``,
                ``search-wanted`` or ``sync``. Bazarr answers an unrecognised action with a 400.
            series_id (int | None, optional): The Sonarr series ID to act on, sent as the ``seriesid``
                parameter. Required for every action except ``search-wanted``, which searches every
                wanted series and ignores the ID. Defaults to None.

        Returns:
            None: Bazarr returns a 204 No Content on success.

        Raises:
            PyarrMissingArgument: If ``series_id`` is omitted for an action that acts on one series.
                Bazarr itself answers such a request with a 204 having done nothing at all.
        """
        if series_id is None and action != "search-wanted":
            raise PyarrMissingArgument(f"series_id must be provided for the '{action}' action")

        params: dict[str, Any] = {"action": action}
        if series_id is not None:
            params["seriesid"] = series_id

        await self.handler.request("series", method="PATCH", params=params)

    async def set_languages_profile(
        self,
        series_id: int | list[int],
        profile_id: int | str | list[int | str],
    ) -> None:
        """Assigns a languages profile to one or more series.

        Bazarr pairs the IDs up by position, so the two arguments must line up. It answers a mismatched
        request with a 500, so the pairing is checked before the request is sent.

        Args:
            series_id (int | list[int]): One or more Sonarr series IDs, sent as the ``seriesid`` parameter,
                repeated once per ID.
            profile_id (int | str | list[int | str]): The languages profile ID for each series, sent as the
                ``profileid`` parameter, repeated once per value. Pass ``"null"`` to clear a series' profile.

        Returns:
            None: Bazarr returns a 204 No Content on success.

        Raises:
            ValueError: If a different number of series IDs and profile IDs is given.
        """
        series_ids = series_id if isinstance(series_id, list) else [series_id]
        profile_ids = profile_id if isinstance(profile_id, list) else [profile_id]
        if len(series_ids) != len(profile_ids):
            raise ValueError("series_id and profile_id must contain the same number of items")

        params: dict[str, Any] = {"seriesid": series_ids, "profileid": profile_ids}

        await self.handler.request("series", method="POST", params=params)
