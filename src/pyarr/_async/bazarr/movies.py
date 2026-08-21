from typing import Any

from pyarr._async.common.base import CommonActions
from pyarr.exceptions import PyarrMissingArgument
from pyarr.literals import BazarrActions
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

    async def run_action(self, action: BazarrActions, movie_id: int | None = None) -> None:
        """Runs an action against a movie, which is how Bazarr is asked to do work.

        Bazarr answers a successful action with a 204 and no body, so there is nothing to return.

        Args:
            action (BazarrActions): The action to run. One of ``scan-disk``, ``search-missing``,
                ``search-wanted`` or ``sync``. Bazarr answers an unrecognised action with a 400.
            movie_id (int | None, optional): The Radarr movie ID to act on, sent as the ``radarrid``
                parameter. Required for every action except ``search-wanted``, which searches every
                wanted movie and ignores the ID. Defaults to None.

        Returns:
            None: Bazarr returns a 204 No Content on success.

        Raises:
            PyarrMissingArgument: If ``movie_id`` is omitted for an action that acts on one movie.
                Bazarr itself answers such a request with a 204 having done nothing at all.
        """
        if movie_id is None and action != "search-wanted":
            raise PyarrMissingArgument(f"movie_id must be provided for the '{action}' action")

        params: dict[str, Any] = {"action": action}
        if movie_id is not None:
            params["radarrid"] = movie_id

        await self.handler.request("movies", method="PATCH", params=params)

    async def set_languages_profile(
        self,
        movie_id: int | list[int],
        profile_id: int | str | list[int | str],
    ) -> None:
        """Assigns a languages profile to one or more movies.

        Bazarr pairs the IDs up by position, so the two arguments must line up. It answers a mismatched
        request with a 500, so the pairing is checked before the request is sent.

        Args:
            movie_id (int | list[int]): One or more Radarr movie IDs, sent as the ``radarrid`` parameter,
                repeated once per ID.
            profile_id (int | str | list[int | str]): The languages profile ID for each movie, sent as the
                ``profileid`` parameter, repeated once per value. Pass ``"null"`` to clear a movie's profile.

        Returns:
            None: Bazarr returns a 204 No Content on success.

        Raises:
            ValueError: If a different number of movie IDs and profile IDs is given.
        """
        movie_ids = movie_id if isinstance(movie_id, list) else [movie_id]
        profile_ids = profile_id if isinstance(profile_id, list) else [profile_id]
        if len(movie_ids) != len(profile_ids):
            raise ValueError("movie_id and profile_id must contain the same number of items")

        params: dict[str, Any] = {"radarrid": movie_ids, "profileid": profile_ids}

        await self.handler.request("movies", method="POST", params=params)
