from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Subtitles(CommonActions):
    """Subtitle actions for Bazarr."""

    async def get(self, **kwargs) -> JsonArray:
        """Returns the list of subtitles.

        Args:
            **kwargs: Additional parameters for filtering.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("subtitles", params=kwargs)
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'subtitles' endpoint")

    async def download(self, subtitle_id: str) -> JsonObject:
        """Download a specific subtitle.

        Args:
            subtitle_id (str): ID of the subtitle to download.

        Returns:
            JsonObject: Download status.
        """
        response = await self.handler.request(f"subtitles/{subtitle_id}", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'subtitles/{subtitle_id}' endpoint")

    async def delete(self, subtitle_id: str) -> None:
        """Delete a specific subtitle.

        Args:
            subtitle_id (str): ID of the subtitle to delete.
        """
        await self.handler.request(f"subtitles/{subtitle_id}", method="DELETE")
