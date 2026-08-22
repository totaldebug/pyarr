from pyarr._async.common.base import CommonActions
from pyarr.types import JsonObject


class Config(CommonActions):
    """Configuration actions shared by every Servarr client.

    Sonarr, Radarr, Lidarr, Readarr, Prowlarr and Whisparr all serve ``config/host``,
    ``config/ui`` and ``config/downloadclient``. Sections that only some of them serve
    live on :class:`MediaConfig` or on the per-application subclasses instead.
    """

    async def _get_section(self, section: str) -> JsonObject:
        """Helper method to read a single configuration section.

        Args:
            section (str): Name of the configuration section, e.g. ``host``.

        Returns:
            JsonObject: Dictionary with the section settings.
        """
        endpoint = f"config/{section}"
        response = await self.handler.request(endpoint)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the '{endpoint}' endpoint")

    async def _update_section(self, section: str, data: JsonObject) -> JsonObject:
        """Helper method to write a single configuration section.

        Args:
            section (str): Name of the configuration section, e.g. ``host``.
            data (JsonObject): Data to be updated within the section.

        Returns:
            JsonObject: Dictionary of the updated section.
        """
        endpoint = f"config/{section}"
        response = await self.handler.request(endpoint, method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the '{endpoint}' endpoint")

    async def get_host(self) -> JsonObject:
        """Get the host configuration, shown as General in the web interface.

        Returns:
            JsonObject: Dictionary with host settings.
        """
        return await self._get_section("host")

    async def update_host(self, data: JsonObject) -> JsonObject:
        """Edit the host configuration.

        Args:
            data (JsonObject): Data to be updated within the host configuration.

        Returns:
            JsonObject: Dictionary of the updated host configuration.
        """
        return await self._update_section("host", data)

    async def get_ui(self) -> JsonObject:
        """Get the UI configuration.

        Returns:
            JsonObject: Dictionary with UI settings.
        """
        return await self._get_section("ui")

    async def update_ui(self, data: JsonObject) -> JsonObject:
        """Edit the UI configuration.

        Args:
            data (JsonObject): Data to be updated within the UI configuration.

        Returns:
            JsonObject: Dictionary of the updated UI configuration.
        """
        return await self._update_section("ui", data)

    async def get_download_client(self) -> JsonObject:
        """Get the download client options.

        Returns:
            JsonObject: Dictionary with download client options.
        """
        return await self._get_section("downloadclient")

    async def update_download_client(self, data: JsonObject) -> JsonObject:
        """Edit the download client options.

        Args:
            data (JsonObject): Data to be updated within the download client options.

        Returns:
            JsonObject: Dictionary of the updated download client options.
        """
        return await self._update_section("downloadclient", data)


class MediaConfig(Config):
    """Configuration actions shared by the media manager clients.

    Sonarr, Radarr, Lidarr, Readarr and Whisparr add the sections that describe how media
    is named and stored. Prowlarr manages no media, so it does not serve these.
    """

    async def get_indexer(self) -> JsonObject:
        """Get the indexer options.

        Returns:
            JsonObject: Dictionary with indexer options.
        """
        return await self._get_section("indexer")

    async def update_indexer(self, data: JsonObject) -> JsonObject:
        """Edit the indexer options.

        Args:
            data (JsonObject): Data to be updated within the indexer options.

        Returns:
            JsonObject: Dictionary of the updated indexer options.
        """
        return await self._update_section("indexer", data)

    async def get_media_management(self) -> JsonObject:
        """Get the media management configuration.

        Returns:
            JsonObject: Dictionary with media management settings.
        """
        return await self._get_section("mediamanagement")

    async def update_media_management(self, data: JsonObject) -> JsonObject:
        """Edit the media management configuration.

        Args:
            data (JsonObject): Data to be updated within the media management configuration.

        Returns:
            JsonObject: Dictionary of the updated media management configuration.
        """
        return await self._update_section("mediamanagement", data)

    async def get_naming(self) -> JsonObject:
        """Get the naming configuration.

        Returns:
            JsonObject: Dictionary with naming settings.
        """
        return await self._get_section("naming")

    async def update_naming(self, data: JsonObject) -> JsonObject:
        """Edit the naming configuration.

        Args:
            data (JsonObject): Data to be updated within the naming configuration.

        Returns:
            JsonObject: Dictionary of the updated naming configuration.
        """
        return await self._update_section("naming", data)

    async def get_naming_examples(self, params: dict | None = None) -> JsonObject:
        """Get naming examples for the supplied naming format.

        Args:
            params (dict | None, optional): Naming format to preview, as sent by the
                naming settings page. Defaults to None, which previews the saved format.

        Returns:
            JsonObject: Dictionary with the rendered examples.
        """
        endpoint = "config/naming/examples"
        response = await self.handler.request(endpoint, params=params)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the '{endpoint}' endpoint")
