from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class MetadataProfile(CommonActions):
    """Metadata profile actions for Lidarr.

    Lidarr's metadata profiles decide which album types and release statuses it
    will consider for an artist. The resource carries ``primaryAlbumTypes``,
    ``secondaryAlbumTypes`` and ``releaseStatuses``, each a list of
    ``{"albumType"|"releaseStatus": {"id", "name"}, "allowed": bool}`` entries,
    so it shares only its endpoint name with Readarr's book-oriented profiles.
    """

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns metadata profiles by ID or all profiles.

        Args:
            item_id (int | None, optional): Database ID for profile. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        return await self._get("metadataprofile", item_id=item_id)

    async def get_schema(self) -> JsonArray | JsonObject:
        """Gets the schema for metadata profiles.

        Returns the album types and release statuses Lidarr knows about, which
        is the starting point for building a profile to pass to `add`.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        response = await self.handler.request("metadataprofile/schema")
        if isinstance(response, list | dict):
            return response
        raise ValueError("Expected a list or dictionary response from the 'metadataprofile/schema' endpoint")

    async def add(self, data: JsonObject) -> JsonObject:
        """Add a new metadata profile.

        Args:
            data (JsonObject): Dictionary with metadata profile settings. Lidarr
                rejects a profile that does not carry the full set of album
                types and release statuses, so build it from `get_schema` or
                from an existing profile returned by `get`.

        Returns:
            JsonObject: Dictionary of added record.
        """
        response = await self.handler.request("metadataprofile", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'metadataprofile' endpoint")

    async def update(self, item_id: int, data: JsonObject) -> JsonObject:
        """Edit a metadata profile by database ID.

        Args:
            item_id (int): Metadata profile database ID.
            data (JsonObject): Data to be updated within the metadata profile.

        Returns:
            JsonObject: Dictionary of updated record.
        """
        response = await self.handler.request(f"metadataprofile/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'metadataprofile/{item_id}' endpoint")

    async def delete(self, item_id: int) -> None:
        """Delete a metadata profile by ID.

        Args:
            item_id (int): Database ID for profile.
        """
        await self._delete("metadataprofile", item_id=item_id)
