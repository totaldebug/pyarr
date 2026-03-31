from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Vod(CommonActions):
    """VOD actions for Dispatcharr."""

    async def get_all(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of all VOD content or a specific item by ID.

        Args:
            item_id (int | None, optional): ID of the VOD item to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("vod/all/", item_id=item_id)

    async def get_categories(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of VOD categories or a specific category by ID.

        Args:
            item_id (int | None, optional): ID of the category to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("vod/categories/", item_id=item_id)

    async def get_episodes(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of VOD episodes or a specific episode by ID.

        Args:
            item_id (int | None, optional): ID of the episode to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("vod/episodes/", item_id=item_id)

    async def get_movies(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of VOD movies or a specific movie by ID.

        Args:
            item_id (int | None, optional): ID of the movie to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("vod/movies/", item_id=item_id)

    async def get_movie_provider_info(self, movie_id: int) -> JsonObject:
        """Retrieve provider info for a specific movie.

        Args:
            movie_id (int): Movie ID.

        Returns:
            JsonObject: The response data.
        """
        return await self._get(f"vod/movies/{movie_id}/provider-info/")

    async def get_movie_providers(self, movie_id: int) -> JsonArray | JsonObject:
        """Retrieve providers for a specific movie.

        Args:
            movie_id (int): Movie ID.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get(f"vod/movies/{movie_id}/providers/")

    async def get_series(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of VOD series or a specific series by ID.

        Args:
            item_id (int | None, optional): ID of the series to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("vod/series/", item_id=item_id)

    async def get_series_episodes(self, series_id: int) -> JsonArray | JsonObject:
        """Retrieve episodes for a specific series.

        Args:
            series_id (int): Series ID.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get(f"vod/series/{series_id}/episodes/")

    async def get_series_provider_info(self, series_id: int) -> JsonObject:
        """Retrieve provider info for a specific series.

        Args:
            series_id (int): Series ID.

        Returns:
            JsonObject: The response data.
        """
        return await self._get(f"vod/series/{series_id}/provider-info/")

    async def get_series_providers(self, series_id: int) -> JsonArray | JsonObject:
        """Retrieve providers for a specific series.

        Args:
            series_id (int): Series ID.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get(f"vod/series/{series_id}/providers/")

    async def get_logos(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of VOD logos or a specific logo by ID.

        Args:
            item_id (int | None, optional): ID of the logo to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("vod/vodlogos/", item_id=item_id)

    async def add_logo(self, data: JsonObject) -> JsonObject:
        """Add a new VOD logo.

        Args:
            data (JsonObject): Logo configuration.

        Returns:
            JsonObject: Added logo details.
        """
        response = await self.handler.request("vod/vodlogos/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'vod/vodlogos/' endpoint")

    async def update_logo(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an existing VOD logo.

        Args:
            item_id (int): Logo ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated logo details.
        """
        response = await self.handler.request(f"vod/vodlogos/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'vod/vodlogos/{item_id}/' endpoint")

    async def partial_update_logo(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update an existing VOD logo.

        Args:
            item_id (int): Logo ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated logo details.
        """
        response = await self.handler.request(f"vod/vodlogos/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'vod/vodlogos/{item_id}/' endpoint")

    async def delete_logo(self, item_id: int) -> None:
        """Delete a VOD logo.

        Args:
            item_id (int): Logo ID.
        """
        await self._delete("vod/vodlogos/", item_id=item_id)

    async def get_logo_cache(self, item_id: int) -> JsonObject:
        """Retrieve cached logo.

        Args:
            item_id (int): Logo ID.

        Returns:
            JsonObject: The response data.
        """
        return await self._get(f"vod/vodlogos/{item_id}/cache/")

    async def bulk_delete_logos(self, ids: list[int]) -> None:
        """Bulk delete VOD logos by ID.

        Args:
            ids (list[int]): List of logo IDs.
        """
        await self.handler.request("vod/vodlogos/bulk-delete/", method="DELETE", json_data={"ids": ids})

    async def cleanup_logos(self, data: JsonObject) -> None:
        """Delete all VOD logos that are not used.

        Args:
            data (JsonObject): Cleanup request data.
        """
        await self.handler.request("vod/vodlogos/cleanup/", method="POST", json_data=data)
