from datetime import datetime

from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray


class Calendar(CommonActions):
    """Calendar actions for Arr clients."""

    async def get(
        self,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        unmonitored: bool = True,
    ) -> JsonArray:
        """Gets upcoming releases.

        Args:
            start_date (datetime | None, optional): Start datetime. Defaults to None.
            end_date (datetime | None, optional): End datetime. Defaults to None.
            unmonitored (bool, optional): Include unmonitored items. Defaults to True.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        params: dict[str, str | bool] = {"unmonitored": unmonitored}
        if start_date:
            params["start"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end"] = end_date.strftime("%Y-%m-%d")

        response = await self.handler.request("calendar", params=params)
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'calendar' endpoint")
