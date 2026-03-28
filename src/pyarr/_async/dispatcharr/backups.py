from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Backups(CommonActions):
    """Backup actions for Dispatcharr."""

    async def get(self) -> JsonArray:
        """List all available backup files.

        Returns:
            JsonArray: The response data.
        """
        return await self._get("backups")

    async def delete(self, filename: str) -> None:
        """Delete a backup file.

        Args:
            filename (str): The name of the backup file to delete.
        """
        await self.handler.request(f"backups/{filename}/delete", method="DELETE")

    async def download(self, filename: str, token: str | None = None) -> JsonObject:
        """Download a backup file.

        Args:
            filename (str): The name of the backup file to download.
            token (str | None, optional): Download token. Defaults to None.

        Returns:
            JsonObject: The response data.
        """
        params = {}
        if token:
            params["download_token"] = token
        return await self._get(f"backups/{filename}/download", params=params)

    async def get_download_token(self, filename: str) -> JsonObject:
        """Get a signed token for downloading a backup file.

        Args:
            filename (str): The name of the backup file.

        Returns:
            JsonObject: The response data.
        """
        return await self._get(f"backups/{filename}/download-token")

    async def restore(self, filename: str) -> JsonObject:
        """Restore from a backup file.

        Args:
            filename (str): The name of the backup file to restore.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request(f"backups/{filename}/restore", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'backups/{filename}/restore' endpoint")

    async def create(self) -> JsonObject:
        """Create a new backup.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("backups/create", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'backups/create' endpoint")

    async def get_schedule(self) -> JsonObject:
        """Get backup schedule settings.

        Returns:
            JsonObject: The response data.
        """
        return await self._get("backups/schedule")

    async def update_schedule(self, data: JsonObject) -> JsonObject:
        """Update backup schedule settings.

        Args:
            data (JsonObject): Schedule settings.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("backups/schedule/update", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'backups/schedule/update' endpoint")

    async def get_status(self, task_id: str, token: str | None = None) -> JsonObject:
        """Check the status of a backup/restore task.

        Args:
            task_id (str): Task ID.
            token (str | None, optional): Task token. Defaults to None.

        Returns:
            JsonObject: The response data.
        """
        params = {}
        if token:
            params["task_token"] = token
        return await self._get(f"backups/status/{task_id}", params=params)

    async def upload(self, data: JsonObject) -> JsonObject:
        """Upload a backup file for restoration.

        Args:
            data (JsonObject): Backup file data.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("backups/upload", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'backups/upload' endpoint")
