from typing import Any

from pyarr._async.common.base import CommonActions
from pyarr.types import JsonObject


class Movies(CommonActions):
    """Movie actions for Bazarr."""

    async def get(self, movie_id: int | list[int] | None = None, **kwargs) -> JsonObject:
        """Returns the movies Bazarr knows about.

        Args:
            movie_id (int | list[int] | None, optional): Limit the results to one or more Radarr movie IDs.
                Sent as the ``radarrid[]`` parameter, repeated once per ID. Defaults to None (all movies).
            **kwargs: Additional parameters, such as ``start`` and ``length`` for paging.

        Returns:
            JsonObject: Dictionary with a ``data`` list of movies and a ``total`` count.
        """
        params: dict[str, Any] = dict(kwargs)
        if movie_id is not None:
            params["radarrid[]"] = movie_id

        response = await self.handler.request("movies", params=params)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'movies' endpoint")
