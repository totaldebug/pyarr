from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Epg(CommonActions):
    """EPG actions for Dispatcharr."""

    async def get_current_programs(self, data: JsonObject) -> JsonArray | JsonObject:
        """Retrieve current programs.

        Args:
            data (JsonObject): Request data.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        response = await self.handler.request("epg/current-programs/", method="POST", json_data=data)
        return response

    async def get_epg_data(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve EPG data.

        Args:
            item_id (int | None, optional): ID of the EPG data to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("epg/epgdata/", item_id=item_id)

    async def get_grid(self) -> JsonArray:
        """Retrieve EPG grid.

        Returns:
            JsonArray: The response data.
        """
        return await self._get("epg/grid/")

    async def import_epg(self, data: JsonObject) -> JsonObject:
        """Import EPG data.

        Args:
            data (JsonObject): Import request data.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("epg/import/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'epg/import/' endpoint")

    async def get_programs(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve EPG programs.

        Args:
            item_id (int | None, optional): ID of the program to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("epg/programs/", item_id=item_id)

    async def add_program(self, data: JsonObject) -> JsonObject:
        """Create a new EPG program.

        Args:
            data (JsonObject): Program data.

        Returns:
            JsonObject: Added program details.
        """
        response = await self.handler.request("epg/programs/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'epg/programs/' endpoint")

    async def update_program(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an EPG program.

        Args:
            item_id (int): Program ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated program details.
        """
        response = await self.handler.request(f"epg/programs/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'epg/programs/{item_id}/' endpoint")

    async def partial_update_program(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update an EPG program.

        Args:
            item_id (int): Program ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated program details.
        """
        response = await self.handler.request(f"epg/programs/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'epg/programs/{item_id}/' endpoint")

    async def delete_program(self, item_id: int) -> None:
        """Delete an EPG program.

        Args:
            item_id (int): Program ID.
        """
        await self._delete("epg/programs/", item_id=item_id)

    async def get_sources(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve EPG sources.

        Args:
            item_id (int | None, optional): ID of the source to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("epg/sources/", item_id=item_id)

    async def add_source(self, data: JsonObject) -> JsonObject:
        """Create a new EPG source.

        Args:
            data (JsonObject): Source data.

        Returns:
            JsonObject: Added source details.
        """
        response = await self.handler.request("epg/sources/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'epg/sources/' endpoint")

    async def update_source(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an EPG source.

        Args:
            item_id (int): Source ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated source details.
        """
        response = await self.handler.request(f"epg/sources/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'epg/sources/{item_id}/' endpoint")

    async def partial_update_source(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update an EPG source.

        Args:
            item_id (int): Source ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated source details.
        """
        response = await self.handler.request(f"epg/sources/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'epg/sources/{item_id}/' endpoint")

    async def delete_source(self, item_id: int) -> None:
        """Delete an EPG source.

        Args:
            item_id (int): Source ID.
        """
        await self._delete("epg/sources/", item_id=item_id)

    async def upload_source(self, data: JsonObject) -> JsonObject:
        """Upload an EPG source.

        Args:
            data (JsonObject): Source file data.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("epg/sources/upload/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'epg/sources/upload/' endpoint")
