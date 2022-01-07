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

        return self.request_get(path, self.ver_uri, params=params)

    def get_system_status(self):
        """Returns system status

        Returns:
            JSON: Array
        """
        path = "system/status"
        return self.request_get(path, self.ver_uri)

    def get_health(self):
        """Query radarr for health information

        Returns:
            JSON: Array
        """
        path = "health"
        return self.request_get(path, self.ver_uri)

    def get_metadata(self):
        """Get all metadata consumer settings

        Returns:
            JSON: Array
        """
        path = "metadata"
        return self.request_get(path, self.ver_uri)

    def get_updates(self):
        """Will return a list of recent updated to Radarr

        Returns:
            JSON: Array
        """
        path = "update"
        return self.request_get(path, self.ver_uri)

    def get_root_folder(self):
        """Get list of root folders, free space and any unmappedFolders

        Returns:
            JSON: Array
        """
        path = "rootfolder"
        return self.request_get(path, self.ver_uri)

    def del_root_folder(self, id_):
        """Delete root folder with specified id

        Args:
            _id (int): Root folder id from database

        Returns:
            JSON: Array
        """
        params = {"id": id_}
        path = "rootfolder"
        return self.request_del(path, self.ver_uri, params=params)

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
        return self.request_get(path, self.ver_uri, params=params)

    def get_disk_space(self):
        """Query disk usage information
            System > Status

        Returns:
            JSON: Array
        """
        path = "diskspace"
        return self.request_get(path, self.ver_uri)

    def get_backup(self):
        """Returns the list of available backups

        Returns:
            JSON: Array
        """
        path = "system/backup"
        return self.request_get(path, self.ver_uri)

    def get_history(
        self, sort_key="date", page=1, page_size=10, sort_dir="desc", id_=None
    ):
        """Gets history (grabs/failures/completed)

        Args:
            sort_key (str, optional): series.title or date. Defaults to "date".
            page (int, optional): Page number to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_dir (str, optional): Direction to sort the items. Defaults to "desc".
            id_ (int, optional): Filter to a specific episode ID. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "history"
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDir": sort_dir,
        }
        if id_:
            params["episodeId"] = id_
        return self.request_get(path, self.ver_uri, params=params)

    def get_blocklist(
        self,
        page=1,
        page_size=20,
        sort_direction="descending",
        sort_key="date",
    ):
        """Returns blocked releases.

        Args:
            page (int, optional): Page to be returned. Defaults to 1.
            page_size (int, optional): Number of results per page. Defaults to 20.
            sort_direction (str, optional): Direction to sort items. Defaults to "descending".
            sort_key (str, optional): Field to sort by. Defaults to "date".

        Returns:
            JSON: Array
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortDirection": sort_direction,
            "sortKey": sort_key,
        }
        path = "blocklist"
        return self.request_get(path, self.ver_uri, params=params)

    def del_blocklist(self, id_):
        """Removes a specific release (the id provided) from the blocklist

        Args:
            id_ (int): blocklist id from database

        Returns:
            JSON: Array
        """
        params = {"id": id_}
        path = "blocklist"
        return self.request_del(path, self.ver_uri, params=params)

    def del_blocklist_bulk(self, data):
        """Delete blocked releases in bulk

        Args:
            data (dict): blocklists that should be deleted

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "blocklist/bulk"
        return self.request_del(path, self.ver_uri, data=data)

    def get_quality_profiles(self):
        """Gets all quality profiles

        Returns:
            JSON: Array
        """
        path = "profile"
        return self.request_get(path, self.ver_uri)

    def get_indexer(self, id_=None):
        """Get all indexers or specific by id_

        Args:
            id_ (int, optional): database if of indexer to return. Defaults to 1None.

        Returns:
            JSON: Array
        """
        path = "indexer" if not id_ else f"indexer/{id_}"
        return self.request_get(path, self.ver_uri)

    def del_indexer(self, id_):
        """Removes a specific indexer from the blocklist

        Args:
            id_ (int): indexer id from database

        Returns:
            JSON: Array
        """
        params = {"id": id_}
        path = "indexer"
        return self.request_del(path, self.ver_uri, params=params)

    def del_queue(self, id_, remove_from_client=True, blacklist=True):
        """Remove an item from the queue and optionally blacklist it

        Args:
            id_ (int): id of the item to be removed
            remove_from_client (bool, optional): Remove the item from the client. Defaults to True.
            blacklist (bool, optional): Add the item to the blacklist. Defaults to True.

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        params = {"removeFromClient": remove_from_client, "blacklist": blacklist}
        path = f"queue/{id_}"
        return self.request_del(path, self.ver_uri, params=params)

    def get_task(self, id_=None):
        """Return a list of tasks, or specify a task ID to return single task

        Args:
            id_ (int): ID for task

        Returns:
            JSON: Array
        """
        path = f"system/task/{id_}" if id_ else "system/task"
        return self.request_get(path, self.ver_uri)

    def get_config_ui(self):
        """Query Radarr for UI settings

        Returns:
            JSON: Array
        """
        path = "config/ui"
        return self.request_get(path, self.ver_uri)

    def upd_config_ui(self, data):
        """Edit one or many UI settings and save to to the database

        Args:
            data (dict): data to be Updated

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "config/ui"
        return self.request_put(path, self.ver_uri, data=data)

    def get_config_host(self):
        """Get General/Host settings.

        Returns:
            JSON: Array
        """
        path = "config/host"
        return self.request_get(path, self.ver_uri)

    def upd_config_host(self, data):
        """Edit General/Host settings.

        Args:
            data (dict): data to bu updated

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "config/host"
        return self.request_put(path, self.ver_uri, data=data)

    def get_config_naming(self):
        """Get Settings for file and folder naming.

        Returns:
            JSON: Array
        """
        path = "config/naming"
        return self.request_get(path, self.ver_uri, self.ver_uri)

    def upd_config_naming(self, data):
        """Edit Settings for file and folder naming.

        Args:
            data (dict): data to be updated

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "config/naming"
        return self.request_put(path, self.ver_uri, data=data)

    def get_notification(self, id_=None):
        """Get all notifications or a single notification by its database id

        Args:
            id_ (int, optional): Notification database id. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "notification" if not id_ else f"notification/{id_}"
        return self.request_get(path, self.ver_uri)

    def upd_notification(self, id_, data):
        """Edit notification by database id

        Args:
            id_ (int): Database id of notification
            data (dict): data that requires updating

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"notification/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    def del_notification(self, id_):
        """Delete a notification by its database id

        Args:
            id_ (int): Database id of notification

        Returns:
            JSON: 201 Ok, 401 Unauthorized
        """
        path = f"notification/{id_}"
        return self.request_del(path, self.ver_uri)

    def get_remote_path_mapping(self):
        """Get a list of remote paths being mapped and used

        Returns:
            JSON: Array
        """
        path = "remotePathMapping"
        return self.request_get(path, self.ver_uri)

    def get_tag(self, id_=None):
        """Returns all tags or specific tag by database id

        Args:
            id_ (int, optional): Database id for tag. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "tag" if not id_ else f"tag/{id_}"
        return self.request_get(path, self.ver_uri)

    def get_tag_detail(self, id_=None):
        """Returns all tags or specific tag by database id with detailed information

        Args:
            id_ (int, optional): Database id for tag. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "tag/detail" if not id_ else f"tag/detail/{id_}"
        return self.request_get(path, self.ver_uri)

    def create_tag(self, label):
        """Adds a new tag

        Args:
            label (str): Tag name / label

        Returns:
            JSON: Array
        """
        data = {"label": label}
        path = "tag"
        return self.request_post(path, self.ver_uri, data=data)

    def upd_tag(self, id_, label):
        """Update an existing tag

        Note:
            You should perform a get_tag() and submit the full body with changes

        Args:
            id_ (int): Database id of tag
            label (str): tag name / label

        Returns:
            JSON: Array
        """
        data = {"id": id_, "label": label}
        path = f"tag/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    def del_tag(self, id_):
        """Delete the tag with the given ID

        Args:
            id_ (int): Database id of tag

        Returns:
            JSON: {}
        """
        path = f"tag/{id_}"
        return self.request_del(path, self.ver_uri)

    def get_download_client(self, id_=None):
        """Get a list of all the download clients or a single client by its database id

        Args:
            id_ (int, optional): Download client database id. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "downloadclient" if not id_ else f"downloadclient/{id_}"
        return self.request_get(path, self.ver_uri)

    def upd_download_client(self, id_, data):
        """Edit a downloadclient by database id

        Args:
            id_ (int): Download client database id
            data (dict): data to be updated within download client

        Returns:
            JSON: 200 Ok
        """
        path = f"downloadclient/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    def del_download_client(self, id_):
        """Delete a download client by database id

        Args:
            id_ (int): download client database id

        Returns:
            JSON: 200 Ok
        """
        path = f"downloadclient/{id_}"
        return self.request_del(path, self.ver_uri)

    def get_import_list(self, id_=None):
        """Query for all lists or a single list by its database id

        Args:
            id_ (int, optional): Import list database id. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "importlist" if not id_ else f"importlist/{id_}"
        return self.request_get(path, self.ver_uri)

    def upd_import_list(self, id_, data):
        """Edit an importlist

        Args:
            id_ (int): Import list database id
            data (dict): data to be updated within the import list

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"importlist/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    def del_import_list(self, id_):
        """Delete an import list

        Args:
            id_ (int): Import list database id

        Returns:
            JSON: 200 ok, 401 Unauthorized
        """
        path = f"importlist/{id_}"
        return self.request_del(path, self.ver_uri)

    def get_media_management(self):
        """Get media managemnet configuration

        Returns:
            JSON: Array
        """
        path = "config/mediamanagement"
        return self.request_get(path, self.ver_uri)
