from datetime import datetime
from .request_api import RequestAPI


class BaseAPI(RequestAPI):
    """Base functions in all Arr api's"""

    def __init__(self, host_url, api_key, ver_uri="/"):

        self.ver_uri = ver_uri
        super().__init__(host_url, api_key)

    def get_calendar(self, start_date=None, end_date=None, unmonitored=True):
        """Gets upcoming releases by monitored, if start/end are not
        supplied, today and tomorrow will be returned

        Args:
            start_date (:obj:`datetime`, optional): ISO8601 start datetime. Defaults to None.
            end_date (:obj:`datetime`, optional): ISO8601 end datetime. Defaults to None.
            unmonitored (bool, optional): Include unmonitored movies. Defaults to True.

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
        params["unmonitored"] = unmonitored

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

    def get_root_folder(self):
        """Query root folder information

        Returns:
            JSON: Array
        """
        path = "rootfolder"
        res = self.request_get(path, self.ver_uri)
        return res

    def get_logs(
        self,
        page=1,
        page_size=10,
        sort_key="time",
        sort_dir="desc",
        filter_key=None,
        filter_value="All",
    ):
        """Gets logs

        Args:
            page (int, optional): Specifiy page to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_key (str, optional): Field to sort by. Defaults to "time".
            sort_dir (str, optional): Direction to sort. Defaults to "desc".
            filter_key (str, optional): Key to filter by. Defaults to None.
            filter_value (str, optional): Value of the filter. Defaults to "All".

        Returns:
            JSON: Array
        """
        path = "log"
        params = {
            "page": page,
            "pageSize": page_size,
            "sortKey": sort_key,
            "sortDir": sort_dir,
            "filterKey": filter_key,
            "filterValue": filter_value,
        }
        res = self.request_get(path, self.ver_uri, params=params)
        return res

    def get_disk_space(self):
        """Query disk usage information
            System > Status

        Returns:
            JSON: Array
        """
        path = "diskspace"
        res = self.request_get(path, self.ver_uri)
        return res

    def get_backup(self):
        """Returns the list of available backups

        Returns:
            JSON: Array
        """
        path = "system/backup"
        res = self.request_get(path, self.ver_uri)
        return res
