from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Proxy(CommonActions):
    """Proxy actions for Dispatcharr."""

    async def get_ts_status(self, channel_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve TS proxy status.

        Args:
            channel_id (int | None, optional): ID of the channel. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        endpoint = "proxy/ts/status/"
        if channel_id:
            endpoint = f"{endpoint}{channel_id}/"
        return await self.handler.request(endpoint, method="GET")

    async def change_ts_stream(self, channel_id: int) -> JsonObject:
        """Change TS stream for a channel.

        Args:
            channel_id (int): Channel ID.

        Returns:
            JsonObject: The response data.
        """
        return await self.handler.request(f"proxy/ts/change_stream/{channel_id}/", method="POST")

    async def next_ts_stream(self, channel_id: int) -> JsonObject:
        """Switch to next TS stream for a channel.

        Args:
            channel_id (int): Channel ID.

        Returns:
            JsonObject: The response data.
        """
        return await self.handler.request(f"proxy/ts/next_stream/{channel_id}/", method="POST")

    async def stop_ts_stream(self, channel_id: int) -> JsonObject:
        """Stop TS stream for a channel.

        Args:
            channel_id (int): Channel ID.

        Returns:
            JsonObject: The response data.
        """
        return await self.handler.request(f"proxy/ts/stop/{channel_id}/", method="POST")

    async def delete_ts_stream(self, channel_id: int) -> None:
        """Delete TS stream for a channel.

        Args:
            channel_id (int): Channel ID.
        """
        await self.handler.request(f"proxy/ts/stop/{channel_id}/", method="DELETE")

    async def stop_ts_client(self, channel_id: int) -> JsonObject:
        """Stop TS client for a channel.

        Args:
            channel_id (int): Channel ID.

        Returns:
            JsonObject: The response data.
        """
        return await self.handler.request(f"proxy/ts/stop_client/{channel_id}/", method="POST")

    async def get_ts_stream(self, channel_id: int) -> JsonObject:
        """Retrieve TS stream for a channel.

        Args:
            channel_id (int): Channel ID.

        Returns:
            JsonObject: The response data.
        """
        return await self.handler.request(f"proxy/ts/stream/{channel_id}/", method="GET")

    async def stop_vod_client(self) -> JsonObject:
        """Stop VOD client.

        Returns:
            JsonObject: The response data.
        """
        return await self.handler.request("proxy/vod/stop_client/", method="POST")
