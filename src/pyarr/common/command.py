from pyarr.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Command(CommonActions):
    """Command actions for Arr clients."""

    def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Queries the status of a previously started command, or all currently started commands.

        Args:
            item_id (int | None, optional): Database ID of the command. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        return self._get("command", item_id=item_id)

    def execute(self, name: str, **kwargs) -> JsonObject:
        """Performs any of the predetermined command routines.

        Args:
            name (str): Command name that should be executed.
            **kwargs: Additional parameters for specific commands.

        Returns:
            JsonObject: Dictionary of command run.
        """
        json_data = {"name": name}
        if kwargs:
            json_data |= kwargs

        response = self.handler.request("command", method="POST", json_data=json_data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'command' endpoint")
