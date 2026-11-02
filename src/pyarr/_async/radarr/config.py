from pyarr._async.common.config import MediaConfig
from pyarr.types import JsonObject


class Config(MediaConfig):
    """Config actions for Radarr.

    Adds the import list and metadata options on top of the shared media manager sections.
    """

    async def get_import_list(self) -> JsonObject:
        """Get the import list options.

        Returns:
            JsonObject: Dictionary with import list options.
        """
        return await self._get_section("importlist")

    async def update_import_list(self, data: JsonObject) -> JsonObject:
        """Edit the import list options.

        Args:
            data (JsonObject): Data to be updated within the import list options.

        Returns:
            JsonObject: Dictionary of the updated import list options.
        """
        return await self._update_section("importlist", data)

    async def get_metadata(self) -> JsonObject:
        """Get the metadata options.

        Returns:
            JsonObject: Dictionary with metadata options.
        """
        return await self._get_section("metadata")

    async def update_metadata(self, data: JsonObject) -> JsonObject:
        """Edit the metadata options.

        Args:
            data (JsonObject): Data to be updated within the metadata options.

        Returns:
            JsonObject: Dictionary of the updated metadata options.
        """
        return await self._update_section("metadata", data)
