from pyarr.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class DelayProfile(CommonActions):
    """Delay profile actions for Readarr."""

    def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns delay profiles by ID or all profiles.

        Args:
            item_id (int | None, optional): Database ID for profile. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        return self._get("delayprofile", item_id=item_id)

    def add(
        self,
        tags: list[int],
        preferred_protocol: str = "usenet",
        usenet_delay: int = 0,
        torrent_delay: int = 0,
        bypass_if_highest_quality: bool = False,
        bypass_if_above_custom_format_score: bool = False,
        minimum_custom_format_score: int = 0,
    ) -> JsonObject:
        """Add a delay profile.

        Args:
            tags (list[int]): List of tag IDs.
            preferred_protocol (str, optional): Preferred protocol. Defaults to "usenet".
            usenet_delay (int, optional): Usenet delay. Defaults to 0.
            torrent_delay (int, optional): Torrent delay. Defaults to 0.
            bypass_if_highest_quality (bool, optional): Bypass if highest quality. Defaults to False.
            bypass_if_above_custom_format_score (bool, optional): Bypass if above score. Defaults to False.
            minimum_custom_format_score (int, optional): Minimum score. Defaults to 0.

        Returns:
            JsonObject: Dictionary of added record.
        """
        json_data = {
            "enableUsenet": True,
            "enableTorrent": True,
            "preferredProtocol": preferred_protocol,
            "usenetDelay": usenet_delay,
            "torrentDelay": torrent_delay,
            "bypassIfHighestQuality": bypass_if_highest_quality,
            "bypassIfAboveCustomFormatScore": bypass_if_above_custom_format_score,
            "minimumCustomFormatScore": minimum_custom_format_score,
            "tags": tags,
        }

        if preferred_protocol == "onlytorrent":
            json_data["preferredProtocol"] = "torrent"
            json_data["enableUsenet"] = False
        elif preferred_protocol == "onlyusenet":
            json_data["preferredProtocol"] = "usenet"
            json_data["enableTorrent"] = False

        response = self.handler.request("delayprofile", method="POST", json_data=json_data)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'delayprofile' endpoint")

    def delete(self, item_id: int) -> None:
        """Delete a delay profile by ID.

        Args:
            item_id (int): Database ID for profile.
        """
        self._delete("delayprofile", item_id=item_id)
