from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Connect(CommonActions):
    """Connect actions for Dispatcharr."""

    async def get_integrations(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve integrations.

        Args:
            item_id (int | None, optional): ID of the integration to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("connect/integrations", item_id=item_id)

    async def add_integration(self, data: JsonObject) -> JsonObject:
        """Create a new integration.

        Args:
            data (JsonObject): Integration data.

        Returns:
            JsonObject: Added integration details.
        """
        response = await self.handler.request("connect/integrations", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'connect/integrations' endpoint")

    async def update_integration(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update an integration.

        Args:
            item_id (int): Integration ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated integration details.
        """
        response = await self.handler.request(f"connect/integrations/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'connect/integrations/{item_id}' endpoint")

    async def partial_update_integration(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update an integration.

        Args:
            item_id (int): Integration ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated integration details.
        """
        response = await self.handler.request(f"connect/integrations/{item_id}", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'connect/integrations/{item_id}' endpoint")

    async def delete_integration(self, item_id: int) -> None:
        """Delete an integration.

        Args:
            item_id (int): Integration ID.
        """
        await self._delete("connect/integrations", item_id=item_id)

    async def get_integration_subscriptions(self, item_id: int) -> JsonArray | JsonObject:
        """Retrieve subscriptions for a specific integration.

        Args:
            item_id (int): Integration ID.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get(f"connect/integrations/{item_id}/subscriptions")

    async def update_integration_subscriptions(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update subscriptions for an integration.

        Args:
            item_id (int): Integration ID.
            data (JsonObject): Subscription data.

        Returns:
            JsonObject: Updated details.
        """
        response = await self.handler.request(
            f"connect/integrations/{item_id}/subscriptions/set",
            method="PUT",
            json_data=data,
        )
        if isinstance(response, dict):
            return response
        raise ValueError(
            f"Expected a dictionary response from the 'connect/integrations/{item_id}/subscriptions/set' endpoint"
        )

    async def test_integration(self, item_id: int) -> JsonObject:
        """Test an integration.

        Args:
            item_id (int): Integration ID.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request(f"connect/integrations/{item_id}/test", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'connect/integrations/{item_id}/test' endpoint")

    async def get_logs(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve connect logs.

        Args:
            item_id (int | None, optional): ID of the log to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("connect/logs", item_id=item_id)

    async def get_subscriptions(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve subscriptions.

        Args:
            item_id (int | None, optional): ID of the subscription to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("connect/subscriptions", item_id=item_id)

    async def add_subscription(self, data: JsonObject) -> JsonObject:
        """Create a new subscription.

        Args:
            data (JsonObject): Subscription data.

        Returns:
            JsonObject: Added subscription details.
        """
        response = await self.handler.request("connect/subscriptions", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'connect/subscriptions' endpoint")

    async def update_subscription(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update a subscription.

        Args:
            item_id (int): Subscription ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated subscription details.
        """
        response = await self.handler.request(f"connect/subscriptions/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'connect/subscriptions/{item_id}' endpoint")

    async def partial_update_subscription(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update a subscription.

        Args:
            item_id (int): Subscription ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated subscription details.
        """
        response = await self.handler.request(f"connect/subscriptions/{item_id}", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'connect/subscriptions/{item_id}' endpoint")

    async def delete_subscription(self, item_id: int) -> None:
        """Delete a subscription.

        Args:
            item_id (int): Subscription ID.
        """
        await self._delete("connect/subscriptions", item_id=item_id)
