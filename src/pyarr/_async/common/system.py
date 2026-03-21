from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class System(CommonActions):
    """System actions for Arr clients."""

    async def get_status(self) -> JsonObject:
        """Gets system status.

        Returns:
           JsonObject: Dictionary with items.
        """
        return await self._get("system/status")

    async def get_health(self) -> JsonArray:
        """Get health information.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        return await self._get("health")

    async def get_diskspace(self) -> JsonArray:
        """Get diskspace information.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        return await self._get("diskspace")

    async def get_task(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Get task information.

        Args:
            item_id (int | None, optional): Get specific task by ID. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        return await self._get("system/task", item_id=item_id)

    async def request_restart(self) -> JsonObject:
        """Request system restart.

        Returns:
            JsonObject: The response data.
        """
        endpoint = "system/restart"
        response = await self.handler.request(endpoint, method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the '{endpoint}' endpoint")

    async def request_shutdown(self) -> JsonObject:
        """Request system shutdown.

        Returns:
            JsonObject: The response data.
        """
        endpoint = "system/shutdown"
        response = await self.handler.request(endpoint, method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the '{endpoint}' endpoint")

    async def get_routes(self) -> JsonObject:
        """Gets system routes.

        Returns:
            JsonObject: dict with all routes.
        """
        return await self._get("system/routes")

    async def get_routes_duplicate(self) -> JsonObject:
        """Gets system routes duplicate.

        Returns:
            JsonObject: dict with routes duplicate.
        """
        return await self._get("system/routes/duplicate")
