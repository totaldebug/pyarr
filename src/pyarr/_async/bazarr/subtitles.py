from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray


class Subtitles(CommonActions):
    """Subtitle actions for Bazarr.

    Bazarr has no ``subtitles/{id}`` route, so a subtitle cannot be downloaded or deleted
    on its own. Those actions belong to the media the subtitle is attached to and live on
    :class:`pyarr._async.bazarr.episodes.Episodes` and
    :class:`pyarr._async.bazarr.movies.Movies` instead.
    """

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
