from pyarr._async.common.config import MediaConfig
from pyarr.types import JsonObject


class Config(MediaConfig):
    """Config actions for Sonarr.

    Adds the import list options on top of the shared media manager sections.
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
