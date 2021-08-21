from datetime import datetime
from .request_api import RequestAPI


class BaseAPI(RequestAPI):
    """Base functions in all Arr api's"""

    def __init__(self, host_url, api_key, ver_uri="/"):

        self.ver_uri = ver_uri
        super().__init__(host_url, api_key)

    def get_calendar(self, start_date=None, end_date=None):
        """Gets upcoming releases by monitored, if start/end are not
        supplied, today and tomorrow will be returned

        Args:
            start_date (:obj:`datetime`, optional): ISO8601 start datetime. Defaults to None.
            end_date (:obj:`datetime`, optional): ISO8601 end datetime. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "calendar"
        params = {}
        if start_date:
            params["start"] = datetime.strptime(start_date, "%Y-%m-%d").strftime(
                "%Y-%m-%d"
            )
        if end_date:
            params["end"] = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")

        res = self.request_get(path, self.ver_uri, params=params)
        return res

    def get_system_status(self):
        """Returns system status

        Returns:
            JSON: Array
        """
        path = "system/status"
        res = self.request_get(path, self.ver_uri)
        return res

    def get_health(self):
        """Query radarr for health information

        Returns:
            JSON: Array
        """
        path = "health"
        res = self.request_get(path, self.ver_uri)
        return res

    def get_metadata(self):
        """Get all metadata consumer settings

        Returns:
            JSON: Array
        """
        path = "metadata"
        res = self.request_get(path, self.ver_uri)
        return res

    def get_updates(self):
        """Will return a list of recent updated to Radarr

        Returns:
            JSON: Array
        """
        path = "update"
        res = self.request_get(path, self.ver_uri)
        return res
