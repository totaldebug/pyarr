from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Hdhr(CommonActions):
    """HDHR actions for Dispatcharr."""

    async def get_device_xml(self) -> JsonObject:
        """Retrieve HDHR device XML.

        Returns:
            JsonObject: The response data.
        """
        return await self._get("hdhr/device.xml/")

    async def get_devices(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve HDHR devices.

        Args:
            item_id (int | None, optional): ID of the device to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("hdhr/devices/", item_id=item_id)

    async def add_device(self, data: JsonObject) -> JsonObject:
        """Create a new HDHR device.

        Args:
            data (JsonObject): Device data.

        Returns:
            JsonObject: Added device details.
        """
        response = await self.handler.request("hdhr/devices/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'hdhr/devices/' endpoint")

    async def update_device(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an HDHR device.

        Args:
            item_id (int): Device ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated device details.
        """
        response = await self.handler.request(f"hdhr/devices/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'hdhr/devices/{item_id}/' endpoint")

    async def partial_update_device(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update an HDHR device.

        Args:
            item_id (int): Device ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated device details.
        """
        response = await self.handler.request(f"hdhr/devices/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'hdhr/devices/{item_id}/' endpoint")

    async def delete_device(self, item_id: int) -> None:
        """Delete an HDHR device.

        Args:
            item_id (int): Device ID.
        """
        await self._delete("hdhr/devices/", item_id=item_id)

    async def discover(self) -> JsonObject:
        """Retrieve HDHR discover JSON.

        Returns:
            JsonObject: The response data.
        """
        return await self._get("hdhr/discover.json/")

    async def get_lineup(self) -> JsonArray:
        """Retrieve HDHR lineup JSON.

        Returns:
            JsonArray: The response data.
        """
        return await self._get("hdhr/lineup.json/")

    async def get_lineup_status(self) -> JsonObject:
        """Retrieve HDHR lineup status JSON.

        Returns:
            JsonObject: The response data.
        """
        return await self._get("hdhr/lineup_status.json/")
