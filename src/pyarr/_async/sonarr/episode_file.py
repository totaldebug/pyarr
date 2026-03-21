from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class EpisodeFile(CommonActions):
    """Episode file actions for Sonarr."""

    async def get(self, item_id: int | None = None, series_id: int | None = None) -> JsonArray | JsonObject:
        """Returns episode file information.

        Args:
            item_id (int | None, optional): Database id of episode file. Defaults to None.
            series_id (int | None, optional): Database id of series. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        params = {}
        if series_id:
            params["seriesId"] = series_id

        return await self._get("episodefile", item_id=item_id, params=params)

    async def delete(self, item_id: int) -> None:
        """Deletes the episode file with corresponding id.

        Args:
            item_id (int): Database id for episode file.
        """
        await self._delete("episodefile", item_id=item_id)

    async def update_quality(self, item_id: int, data: JsonObject) -> JsonObject:
        """Updates the quality of the episode file.

        Args:
            item_id (int): Database id for episode file.
            data (JsonObject): Data with quality.

        Returns:
            JsonObject: Dictionary with updated record.
        """
        response = await self.handler.request(f"episodefile/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'episodefile/{item_id}' endpoint")
