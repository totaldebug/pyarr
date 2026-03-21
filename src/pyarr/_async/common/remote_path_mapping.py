from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class RemotePathMapping(CommonActions):
    """Remote path mapping actions for Arr clients."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns the list of remote path mappings or a specific mapping by ID.

        Args:
            item_id (int | None, optional): ID of the mapping to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("remotepathmapping", item_id=item_id)
