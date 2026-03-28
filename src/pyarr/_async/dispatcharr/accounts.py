from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Accounts(CommonActions):
    """Account actions for Dispatcharr."""

    async def get_api_keys(self) -> JsonObject:
        """Retrieve API keys.

        Returns:
            JsonObject: The response data.
        """
        return await self._get("accounts/api-keys")

    async def generate_api_key(self) -> JsonObject:
        """Generate a new API key.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("accounts/api-keys/generate", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'accounts/api-keys/generate' endpoint")

    async def revoke_api_key(self) -> JsonObject:
        """Revoke an API key.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("accounts/api-keys/revoke", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'accounts/api-keys/revoke' endpoint")

    async def login(self, data: JsonObject) -> JsonObject:
        """Authenticate and log in a user.

        Args:
            data (JsonObject): Login request data.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("accounts/auth/login", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'accounts/auth/login' endpoint")

    async def logout(self) -> JsonObject:
        """Log out the current user.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("accounts/auth/logout", method="POST")
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'accounts/auth/logout' endpoint")

    async def get_groups(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve a list of groups or a specific group by ID.

        Args:
            item_id (int | None, optional): ID of the group to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("accounts/groups", item_id=item_id)

    async def add_group(self, data: JsonObject) -> JsonObject:
        """Create a new group.

        Args:
            data (JsonObject): Group data.

        Returns:
            JsonObject: Added group details.
        """
        response = await self.handler.request("accounts/groups", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'accounts/groups' endpoint")

    async def update_group(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update a group.

        Args:
            item_id (int): Group ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated group details.
        """
        response = await self.handler.request(f"accounts/groups/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'accounts/groups/{item_id}' endpoint")

    async def partial_update_group(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update a group.

        Args:
            item_id (int): Group ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated group details.
        """
        response = await self.handler.request(f"accounts/groups/{item_id}", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'accounts/groups/{item_id}' endpoint")

    async def delete_group(self, item_id: int) -> None:
        """Delete a group.

        Args:
            item_id (int): Group ID.
        """
        await self._delete("accounts/groups", item_id=item_id)

    async def get_permissions(self) -> JsonArray:
        """Retrieve a list of all permissions.

        Returns:
            JsonArray: The response data.
        """
        return await self._get("accounts/permissions")

    async def create_token(self, data: JsonObject) -> JsonObject:
        """Takes a set of user credentials and returns an access and refresh JSON web token pair.

        Args:
            data (JsonObject): Token obtain pair data.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("accounts/token", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'accounts/token' endpoint")

    async def refresh_token(self, data: JsonObject) -> JsonObject:
        """Takes a refresh type JSON web token and returns an access type JSON web token.

        Args:
            data (JsonObject): Token refresh data.

        Returns:
            JsonObject: The response data.
        """
        response = await self.handler.request("accounts/token/refresh", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'accounts/token/refresh' endpoint")

    async def get_users(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Retrieve a list of users or a specific user by ID.

        Args:
            item_id (int | None, optional): ID of the user to return. Defaults to None.

        Returns:
            JsonArray | JsonObject: The response data.
        """
        return await self._get("accounts/users", item_id=item_id)

    async def add_user(self, data: JsonObject) -> JsonObject:
        """Create a new user.

        Args:
            data (JsonObject): User data.

        Returns:
            JsonObject: Added user details.
        """
        response = await self.handler.request("accounts/users", method="POST", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'accounts/users' endpoint")

    async def update_user(self, item_id: int, data: JsonObject) -> JsonObject:
        """Update a user.

        Args:
            item_id (int): User ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated user details.
        """
        response = await self.handler.request(f"accounts/users/{item_id}", method="PUT", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'accounts/users/{item_id}' endpoint")

    async def partial_update_user(self, item_id: int, data: JsonObject) -> JsonObject:
        """Partially update a user.

        Args:
            item_id (int): User ID.
            data (JsonObject): Updated configuration.

        Returns:
            JsonObject: Updated user details.
        """
        response = await self.handler.request(f"accounts/users/{item_id}", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError(f"Expected a dictionary response from the 'accounts/users/{item_id}' endpoint")

    async def delete_user(self, item_id: int) -> None:
        """Delete a user.

        Args:
            item_id (int): User ID.
        """
        await self._delete("accounts/users", item_id=item_id)

    async def get_me(self) -> JsonObject:
        """Get active user information.

        Returns:
            JsonObject: The response data.
        """
        return await self._get("accounts/users/me")

    async def partial_update_me(self, data: JsonObject) -> JsonObject:
        """Update active user information.

        Args:
            data (JsonObject): Patched user data.

        Returns:
            JsonObject: Updated user details.
        """
        response = await self.handler.request("accounts/users/me", method="PATCH", json_data=data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'accounts/users/me' endpoint")
