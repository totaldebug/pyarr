from pyarr._async.common.config import MediaConfig
from pyarr.types import JsonObject


class Config(MediaConfig):
    """Config actions for Lidarr.

    Adds the metadata provider options on top of the shared media manager sections.
    """

    async def get_metadata_provider(self) -> JsonObject:
        """Get the metadata provider options.

        Returns:
            JsonObject: Dictionary with metadata provider options.
        """
        return await self._get_section("metadataProvider")

    async def update_metadata_provider(self, data: JsonObject) -> JsonObject:
        """Edit the metadata provider options.

        Args:
            data (JsonObject): Data to be updated within the metadata provider options.

        Returns:
            JsonObject: Dictionary of the updated metadata provider options.
        """
        return await self._update_section("metadataProvider", data)
