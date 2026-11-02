from pyarr._async.common.config import Config as CommonConfig
from pyarr.types import JsonObject


class Config(CommonConfig):
    """Config actions for Prowlarr.

    Prowlarr manages no media, so it serves only the shared sections plus the
    development options. The media manager sections are deliberately absent.
    """

    async def get_development(self) -> JsonObject:
        """Get the development options.

        Returns:
            JsonObject: Dictionary with development options.
        """
        return await self._get_section("development")

    async def update_development(self, data: JsonObject) -> JsonObject:
        """Edit the development options.

        Args:
            data (JsonObject): Data to be updated within the development options.

        Returns:
            JsonObject: Dictionary of the updated development options.
        """
        return await self._update_section("development", data)
