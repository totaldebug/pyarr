from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class MovieFile(CommonActions):
    """Movie file actions for Radarr."""

    async def get(self, item_id: int | None = None, movie_id: int | None = None) -> JsonArray | JsonObject:
        """Returns movie file information.

        Args:
            item_id (int | None, optional): Database id of movie file. Defaults to None.
            movie_id (int | None, optional): Database id of movie. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        params = {}
        if movie_id:
            params["movieId"] = movie_id

        return await self._get("moviefile", item_id=item_id, params=params)

    async def delete(self, item_id: int) -> None:
        """Deletes the movie file with corresponding id.

        Args:
            item_id (int): Database id for movie file.
        """
        await self._delete("moviefile", item_id=item_id)
