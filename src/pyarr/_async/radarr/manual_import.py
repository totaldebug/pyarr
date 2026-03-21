from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class ManualImport(CommonActions):
    """Manual import actions for Radarr."""

    async def get(
        self,
        folder: str,
        download_id: str | None = None,
        movie_id: int | None = None,
        filter_existing_files: bool = True,
        replace_existing_files: bool = True,
    ) -> JsonArray:
        """Gets a manual import list.

        Args:
            folder (str): Folder name.
            download_id (str | None, optional): Download ID. Defaults to None.
            movie_id (int | None, optional): Movie Database ID. Defaults to None.
            filter_existing_files (bool, optional): Filter files. Defaults to True.
            replace_existing_files (bool, optional): Replace files. Defaults to True.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        params: dict[str, str | int | bool] = {"folder": folder}
        if download_id:
            params["downloadId"] = download_id
        if movie_id:
            params["movieId"] = movie_id

        params["filterExistingFiles"] = filter_existing_files
        params["replaceExistingFiles"] = replace_existing_files

        response = await self.handler.request("manualimport", params=params)
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'manualimport' endpoint")

    async def update(self, data: JsonObject) -> JsonObject:
        """Update a manual import.

        Args:
            data (JsonObject): Data containing changes.

        Returns:
            JsonObject: Dictionary of updated record.
        """
        response = await self.handler.request("manualimport", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'manualimport' endpoint")
