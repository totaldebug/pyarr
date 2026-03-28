from pyarr._async.common.indexer import Indexer as CommonIndexer
from pyarr.types import JsonArray, JsonObject


class Indexer(CommonIndexer):
    """Indexer actions for Prowlarr."""

    async def get_stats(self) -> JsonObject:
        """Gets indexer stats.

        Returns:
            JsonObject: Dictionary with indexer stats.
        """
        return await self._get("indexerstats")

    async def get_status(self) -> JsonArray:
        """Gets indexer status.

        Returns:
            JsonArray: List of dictionaries with indexer status.
        """
        return await self._get("indexerstatus")
