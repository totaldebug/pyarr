from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class DispatcharrSystem(CommonActions):
    """System actions for Dispatcharr (Core API)."""

    async def get_notifications(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve notifications.

        Args:
            item_id (int | None, optional): ID of the notification to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("core/notifications/", item_id=item_id)

    async def add_notification(self, data: JsonObject) -> JsonObject:
        """Create a new notification.

        Args:
            data (JsonObject): Notification data.

        Returns:
            JsonObject: Added notification details.
        """
        response = await self.handler.request("core/notifications/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'core/notifications/' endpoint")

    async def update_notification(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update a notification.

        Args:
            item_id (int): Notification ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated notification details.
        """
        response = await self.handler.request(f"core/notifications/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'core/notifications/{item_id}/' endpoint")

    async def partial_update_notification(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update a notification.

        Args:
            item_id (int): Notification ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated notification details.
        """
        response = await self.handler.request(f"core/notifications/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'core/notifications/{item_id}/' endpoint")

    async def delete_notification(self, item_id: int) -> None:
        """Delete a notification.

        Args:
            item_id (int): Notification ID.
        """
        await self._delete("core/notifications/", item_id=item_id)

    async def dismiss_notification(self, item_id: int) -> JsonObject:
        """Dismiss a notification.

        Args:
            item_id (int): Notification ID.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request(f"core/notifications/{item_id}/dismiss/", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'core/notifications/{item_id}/dismiss/' endpoint")

    async def get_notification_count(self) -> JsonObject:
        """Retrieve notification count.

        Returns:
            JsonObject: The response data.
        """
        return await self._get("core/notifications/count/")

    async def dismiss_all_notifications(self) -> JsonObject:
        """Dismiss all notifications.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("core/notifications/dismiss-all/", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'core/notifications/dismiss-all/' endpoint")

    async def rehash_streams(self) -> JsonObject:
        """Rehash streams.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("core/rehash-streams/", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'core/rehash-streams/' endpoint")

    async def get_settings(self, item_id: str | None = None) -> JsonArray | JsonObject:
        """Retrieve settings.

        Args:
            item_id (str | None, optional): ID of the setting to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("core/settings/", item_id=item_id)

    async def add_setting(self, data: JsonObject) -> JsonObject:
        """Create a new setting.

        Args:
            data (JsonObject): Setting data.

        Returns:
            JsonObject: Added setting details.
        """
        response = await self.handler.request("core/settings/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'core/settings/' endpoint")

    async def update_setting(self, item_id: str, data: JsonObject) -> JsonObject:
        """Update a setting.

        Args:
            item_id (str): Setting ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated notification details.
        """
        response = await self.handler.request(f"core/settings/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'core/settings/{item_id}/' endpoint")

    async def partial_update_setting(self, item_id: str, data: JsonObject) -> JsonObject:
        """Partially update a setting.

        Args:
            item_id (str): Setting ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated notification details.
        """
        response = await self.handler.request(f"core/settings/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'core/settings/{item_id}/' endpoint")

    async def delete_setting(self, item_id: str) -> None:
        """Delete a setting.

        Args:
            item_id (str): Setting ID.
        """
        await self._delete("core/settings/", item_id=item_id)

    async def check_settings(self) -> JsonObject:
        """Check settings.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("core/settings/check/", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'core/settings/check/' endpoint")

    async def get_env(self) -> JsonObject:
        """Retrieve environment variables.

        Returns:
            JsonObject: The response data.
        """
        return await self._get("core/settings/env/")

    async def get_stream_profiles(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve stream profiles.

        Args:
            item_id (int | None, optional): ID of the profile to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("core/streamprofiles/", item_id=item_id)

    async def add_stream_profile(self, data: JsonObject) -> JsonObject:
        """Create a new stream profile.

        Args:
            data (JsonObject): Profile data.

        Returns:
            JsonObject: Added profile details.
        """
        response = await self.handler.request("core/streamprofiles/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'core/streamprofiles/' endpoint")

    async def update_stream_profile(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update a stream profile.

        Args:
            item_id (int): Profile ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated profile details.
        """
        response = await self.handler.request(f"core/streamprofiles/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'core/streamprofiles/{item_id}/' endpoint")

    async def partial_update_stream_profile(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update a stream profile.

        Args:
            item_id (int): Profile ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated profile details.
        """
        response = await self.handler.request(f"core/streamprofiles/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'core/streamprofiles/{item_id}/' endpoint")

    async def delete_stream_profile(self, item_id: int) -> None:
        """Delete a stream profile.

        Args:
            item_id (int): Profile ID.
        """
        await self._delete("core/streamprofiles/", item_id=item_id)

    async def get_system_events(self) -> JsonArray:
        """Retrieve system events.

        Returns:
            JsonArray: The response data.
        """
        return await self._get("core/system-events/")

    async def get_timezones(self) -> JsonArray:
        """Retrieve timezones.

        Returns:
            JsonArray: The response data.
        """
        return await self._get("core/timezones/")

    async def get_user_agents(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve user agents.

        Args:
            item_id (int | None, optional): ID of the user agent to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("core/useragents/", item_id=item_id)

    async def add_user_agent(self, data: JsonObject) -> JsonObject:
        """Create a new user agent.

        Args:
            data (JsonObject): User agent data.

        Returns:
            JsonObject: Added user agent details.
        """
        response = await self.handler.request("core/useragents/", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'core/useragents/' endpoint")

    async def update_user_agent(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update a user agent.

        Args:
            item_id (int): User agent ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated user agent details.
        """
        response = await self.handler.request(f"core/useragents/{item_id}/", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'core/useragents/{item_id}/' endpoint")

    async def partial_update_user_agent(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update a user agent.

        Args:
            item_id (int): User agent ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated user agent details.
        """
        response = await self.handler.request(f"core/useragents/{item_id}/", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'core/useragents/{item_id}/' endpoint")

    async def delete_user_agent(self, item_id: int) -> None:
        """Delete a user agent.

        Args:
            item_id (int): User agent ID.
        """
        await self._delete("core/useragents/", item_id=item_id)

    async def get_version(self) -> JsonObject:
        """Retrieve version information.

        Returns:
            JsonObject: The response data.
        """
        return await self._get("core/version/")
