from datetime import datetime
from typing import Any

from requests import Response

from .request_handler import RequestHandler


class BaseArrAPI(RequestHandler):
    """Base functions in all Arr API's"""

    def __init__(self, host_url, api_key, ver_uri="/"):

        self.ver_uri = ver_uri
        super().__init__(host_url, api_key)

    # CALENDAR

    # GET /calendar/
    def get_calendar(
        self, start_date=None, end_date=None, unmonitored=True
    ) -> list[dict] | Any:
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

    # SYSTEM

    # GET /system/status
    def get_system_status(self) -> list[dict] | Any:
        """Returns system status

        Returns:
            JSON: Array
        """
        path = "system/status"
        return self.request_get(path, self.ver_uri)

    # GET /health
    def get_health(self) -> list[dict] | Any:
        """Query radarr for health information

        Returns:
            JSON: Array
        """
        path = "health"
        return self.request_get(path, self.ver_uri)

    # GET /metadata
    def get_metadata(self) -> list[dict] | Any:
        """Get all metadata consumer settings

        Returns:
            JSON: Array
        """
        path = "metadata"
        return self.request_get(path, self.ver_uri)

    # GET /update
    def get_update(self) -> list[dict] | Any:
        """Will return a list of recent updated to Radarr

        Returns:
            JSON: Array
        """
        path = "update"
        return self.request_get(path, self.ver_uri)

    # GET /rootfolder
    def get_root_folder(self) -> list[dict] | Any:
        """Get list of root folders, free space and any unmappedFolders

        Returns:
            JSON: Array
        """
        path = "rootfolder"
        return self.request_get(path, self.ver_uri)

    # DELETE /rootfolder
    def del_root_folder(
        self, id_
    ) -> list[dict] | Any:  # sourcery skip: class-extract-method
        """Delete root folder with specified id

        Args:
            _id (int): Root folder id from database

        Returns:
            JSON: Array
        """
        params = {"id": id_}
        path = "rootfolder"
        return self.request_del(path, self.ver_uri, params=params)

    # GET /diskspace
    def get_disk_space(self) -> list[dict] | Any:
        """Query disk usage information
            System > Status

        Returns:
            JSON: Array
        """
        path = "diskspace"
        return self.request_get(path, self.ver_uri)

    # GET /system/backup
    def get_backup(self) -> list[dict] | Any:
        """Returns the list of available backups

        Returns:
            JSON: Array
        """
        path = "system/backup"
        return self.request_get(path, self.ver_uri)

    # LOGS

    # GET /log
    def get_log(
        self,
        page=1,
        page_size=10,
        sort_key="time",
        sort_dir="desc",
        filter_key=None,
        filter_value="All",
    ) -> list[dict] | Any:
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

    # GET /history
    def get_history(
        self, sort_key="date", page=1, page_size=10, sort_dir="desc", id_=None
    ) -> list[dict] | Any:
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

    # BLOCKLIST

    # GET /blocklist
    def get_blocklist(
        self,
        page=1,
        page_size=20,
        sort_direction="descending",
        sort_key="date",
    ) -> list[dict] | Any:
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

    # DELETE /blocklist
    def del_blocklist(self, id_) -> list[dict] | Any:
        """Removes a specific release (the id provided) from the blocklist

        Args:
            id_ (int): blocklist id from database

        Returns:
            JSON: Array
        """
        params = {"id": id_}
        path = "blocklist"
        return self.request_del(path, self.ver_uri, params=params)

    # DELETE /blocklist/bulk
    def del_blocklist_bulk(self, data) -> Response | Any:
        """Delete blocked releases in bulk

        Args:
            data (dict): blocklists that should be deleted

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "blocklist/bulk"
        return self.request_del(path, self.ver_uri, data=data)

    # PROFILES

    # GET /qualityprofile/{id}
    def get_quality_profile(self, id_=None) -> list[dict] | Any:
        """Gets all quality profiles or specific one with id_

        Args:
            id_ (int): quality profile id from database

        Returns:
            JSON: Array
        """
        path = "qualityprofile" if not id_ else f"qualityprofile/{id_}"
        return self.request_get(path, self.ver_uri)

    # PUT /qualityprofile/{id}
    def upd_quality_profile(self, id_, data) -> list[dict] | Any:
        """Update the quality profile data.

        Note:
            To be used in conjunction with get_quality_profile()

        Args:
            id_ (int): Profile ID to Update
            data (dict): All parameters to update

        Returns:
            JSON: Array
        """
        path = f"qualityprofile/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    # DELETE /qualityprofile
    def del_quality_profile(self, id_) -> list[dict] | Any:
        """Removes a specific quality profile from the blocklist

        Args:
            id_ (int): quality profile id from database

        Returns:
            JSON: Array
        """
        params = {"id": id_}
        path = "qualityprofile"
        return self.request_del(path, self.ver_uri, params=params)

    # GET /qualitydefinition/{id}
    def get_quality_definition(self, id_=None) -> list[dict] | Any:
        """Gets all quality definitions or specific one by ID

        Args:
            id_ (int, optional): Import list database id. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "qualitydefinition" if not id_ else f"qualitydefinition/{id_}"
        return self.request_get(path, self.ver_uri)

    # PUT /qualitydefinition/{id}
    def upd_quality_definition(self, id_, data) -> list[dict] | Any:
        """Update the quality definitions.

        Note:
            To be used in conjunction with get_quality_definition()

        Args:
            id_ (int): ID of definition to update
            data (dict): All parameters to update

        Returns:
            JSON: Array
        """
        path = f"qualitydefinition/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    # INDEXER

    # GET /indexer/{id}
    def get_indexer(self, id_=None) -> list[dict] | Any:
        """Get all indexers or specific by id_

        Args:
            id_ (int, optional): database if of indexer to return. Defaults to 1None.

        Returns:
            JSON: Array
        """
        path = "indexer" if not id_ else f"indexer/{id_}"
        return self.request_get(path, self.ver_uri)

    # PUT /indexer/{id}
    def upd_indexer(self, id_, data) -> list[dict] | Any:
        """Edit a Indexer by database id

        Note:
            To be used in conjunction with get_indexer()

        Args:
            id_ (int): Indexer database id
            data (dict): data to be updated within Indexer

        Returns:
            JSON: Array
        """
        path = f"indexer/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    # DELETE /indexer
    def del_indexer(self, id_) -> list[dict] | Any:
        """Removes a specific indexer from the blocklist

        Args:
            id_ (int): indexer id from database

        Returns:
            JSON: Array
        """
        params = {"id": id_}
        path = "indexer"
        return self.request_del(path, self.ver_uri, params=params)

    # QUEUE

    # DELETE /queue/{id}
    def del_queue(
        self, id_, remove_from_client=True, blacklist=True
    ) -> list[dict] | Any:
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

    # GET /system/task/{id}
    def get_task(self, id_=None) -> list[dict] | Any:
        """Return a list of tasks, or specify a task ID to return single task

        Args:
            id_ (int): ID for task

        Returns:
            JSON: Array
        """
        path = f"system/task/{id_}" if id_ else "system/task"
        return self.request_get(path, self.ver_uri)

    # GET /remotePathMapping
    def get_remote_path_mapping(self) -> list[dict] | Any:
        """Get a list of remote paths being mapped and used

        Returns:
            JSON: Array
        """
        path = "remotePathMapping"
        return self.request_get(path, self.ver_uri)

    # CONFIG

    # GET /config/ui
    def get_config_ui(self) -> list[dict] | Any:
        """Query Radarr for UI settings

        Returns:
            JSON: Array
        """
        path = "config/ui"
        return self.request_get(path, self.ver_uri)

    # PUT /config/ui
    def upd_config_ui(self, data) -> Response | Any:
        """Edit one or many UI settings and save to to the database

        Args:
            data (dict): data to be Updated

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "config/ui"
        return self.request_put(path, self.ver_uri, data=data)

    # GET /config/host
    def get_config_host(self) -> list[dict] | Any:
        """Get General/Host settings.

        Returns:
            JSON: Array
        """
        path = "config/host"
        return self.request_get(path, self.ver_uri)

    # PUT /config/host
    def upd_config_host(self, data) -> Response | Any:
        """Edit General/Host settings.

        Args:
            data (dict): data to be updated

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "config/host"
        return self.request_put(path, self.ver_uri, data=data)

    # GET /config/naming
    def get_config_naming(self) -> list[dict] | Any:
        """Get Settings for file and folder naming.

        Returns:
            JSON: Array
        """
        path = "config/naming"
        return self.request_get(path, self.ver_uri, self.ver_uri)

    # PUT /config/naming
    def upd_config_naming(self, data) -> Response | Any:
        """Edit Settings for file and folder naming.

        Args:
            data (dict): data to be updated

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = "config/naming"
        return self.request_put(path, self.ver_uri, data=data)

    # GET /config/mediamanagement
    def get_media_management(self) -> list[dict] | Any:
        """Get media managemnet configuration

        Returns:
            JSON: Array
        """
        path = "config/mediamanagement"
        return self.request_get(path, self.ver_uri)

    # NOTIFICATIONS

    # GET /notification/{id}
    def get_notification(self, id_=None) -> list[dict] | Any:
        """Get all notifications or a single notification by its database id

        Args:
            id_ (int, optional): Notification database id. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "notification" if not id_ else f"notification/{id_}"
        return self.request_get(path, self.ver_uri)

    # GET /notification/schema
    def get_notification_schema(self) -> list[dict] | Any:
        """Get possible notification connections

        Returns:
            JSON: Array
        """
        path = "notification/schema"
        return self.request_get(path, self.ver_uri)

    # PUT /notification/{id}
    def upd_notification(self, id_, data) -> Response | Any:
        """Edit notification by database id

        Args:
            id_ (int): Database id of notification
            data (dict): data that requires updating

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"notification/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    # DELETE /notification/{id}
    def del_notification(self, id_) -> Response | Any:
        """Delete a notification by its database id

        Args:
            id_ (int): Database id of notification

        Returns:
            JSON: 201 Ok, 401 Unauthorized
        """
        path = f"notification/{id_}"
        return self.request_del(path, self.ver_uri)

    # TAGS

    # GET /tag/{id}
    def get_tag(self, id_=None) -> list[dict] | Any:
        """Returns all tags or specific tag by database id

        Args:
            id_ (int, optional): Database id for tag. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "tag" if not id_ else f"tag/{id_}"
        return self.request_get(path, self.ver_uri)

    # GET /tag/detail/{id}
    def get_tag_detail(self, id_=None) -> list[dict] | Any:
        """Returns all tags or specific tag by database id with detailed information

        Args:
            id_ (int, optional): Database id for tag. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "tag/detail" if not id_ else f"tag/detail/{id_}"
        return self.request_get(path, self.ver_uri)

    # POST /tag
    def create_tag(self, label) -> list[dict] | Any:
        """Adds a new tag

        Args:
            label (str): Tag name / label

        Returns:
            JSON: Array
        """
        data = {"label": label}
        path = "tag"
        return self.request_post(path, self.ver_uri, data=data)

    # PUT /tag/{id}
    def upd_tag(self, id_, label) -> list[dict] | Any:
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

    # DELETE /tag/{id}
    def del_tag(self, id_) -> dict | Any:
        """Delete the tag with the given ID

        Args:
            id_ (int): Database id of tag

        Returns:
            JSON: {}
        """
        path = f"tag/{id_}"
        return self.request_del(path, self.ver_uri)

    # DOWNLOAD CLIENT

    # GET /downloadclient/{id}
    def get_download_client(self, id_=None) -> list[dict] | Any:
        """Get a list of all the download clients or a single client by its database id

        Args:
            id_ (int, optional): Download client database id. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "downloadclient" if not id_ else f"downloadclient/{id_}"
        return self.request_get(path, self.ver_uri)

    # GET /downloadclient/schema
    def get_download_client_schema(self) -> list[dict] | Any:
        """Get a list of all the supported download clients

        Returns:
            JSON: Array
        """
        path = "downloadclient/schema"
        return self.request_get(path, self.ver_uri)

    # PUT /downloadclient/{id}
    def upd_download_client(self, id_, data) -> Response | Any:
        """Edit a downloadclient by database id

        Args:
            id_ (int): Download client database id
            data (dict): data to be updated within download client

        Returns:
            JSON: 200 Ok
        """
        path = f"downloadclient/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    # DELETE /downloadclient/{id}
    def del_download_client(self, id_) -> Response | Any:
        """Delete a download client by database id

        Args:
            id_ (int): download client database id

        Returns:
            JSON: 200 Ok
        """
        path = f"downloadclient/{id_}"
        return self.request_del(path, self.ver_uri)

    # IMPORT LIST

    # GET /importlist
    def get_import_list(self, id_=None) -> list[dict] | Any:
        """Query for all lists or a single list by its database id

        Args:
            id_ (int, optional): Import list database id. Defaults to None.

        Returns:
            JSON: Array
        """
        path = "importlist" if not id_ else f"importlist/{id_}"
        return self.request_get(path, self.ver_uri)

    # PUT /importlist/{id}
    def upd_import_list(self, id_, data) -> Response | Any:
        """Edit an importlist

        Args:
            id_ (int): Import list database id
            data (dict): data to be updated within the import list

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"importlist/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    # DELETE /importlist/{id}
    def del_import_list(self, id_) -> Response | Any:
        """Delete an import list

        Args:
            id_ (int): Import list database id

        Returns:
            JSON: 200 Ok, 401 Unauthorized
        """
        path = f"importlist/{id_}"
        return self.request_del(path, self.ver_uri)
