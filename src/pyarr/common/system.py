from pyarr.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class System(CommonActions):
    """System actions for Arr clients."""

    def get_status(self) -> JsonObject:
        """Gets system status.

        Returns:
           JsonObject: Dictionary with items.
        """
        return self._get("system/status")

    def get_health(self) -> JsonArray:
        """Get health information.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        return self._get("health")

    def get_diskspace(self) -> JsonArray:
        """Get diskspace information.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        return self._get("diskspace")

    def get_task(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Get task information.

        Args:
            item_id (int | None, optional): Get specific task by ID. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        return self._get("system/task", item_id=item_id)

    def request_restart(self) -> JsonObject:
        """Request system restart.

        Returns:
            JsonObject: The response data.
        """
        endpoint = "system/restart"
        response = self.handler.request(endpoint, method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the '{endpoint}' endpoint")

    def request_shutdown(self) -> JsonObject:
        """Request system shutdown.

        Returns:
            JsonObject: The response data.
        """
        endpoint = "system/shutdown"
        response = self.handler.request(endpoint, method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the '{endpoint}' endpoint")

    def get_routes(self) -> JsonObject:
        """Gets system routes.

        Returns:
            JsonObject: dict with all routes.
        """
        return self._get("system/routes")

    def get_routes_duplicate(self) -> JsonObject:
        """Gets system routes duplicate.

        Returns:
            JsonObject: dict with routes duplicate.
        """
        return self._get("system/routes/duplicate")
