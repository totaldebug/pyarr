from datetime import datetime
from typing import Any, Optional, Union

from requests import Response

from pyarr.exceptions import PyarrMissingArgument, PyarrRecordNotFound
from pyarr.models.common import (
    PyarrBlocklistSortKey,
    PyarrDownloadClientSchema,
    PyarrHistorySortKey,
    PyarrImportListSchema,
    PyarrIndexerSchema,
    PyarrLogFilterKey,
    PyarrLogFilterValue,
    PyarrLogSortKey,
    PyarrNotificationSchema,
    PyarrSortDirection,
)
from pyarr.models.lidarr import LidarrImportListSchema
from pyarr.types import JsonArray, JsonObject

from .request_handler import RequestHandler


class BaseArrAPI(RequestHandler):
    """Base functions in all Arr API's"""

    def __init__(self, host_url: str, api_key: str, ver_uri: str = "/"):
        """Initialise the instance connection

        Args:
            host_url (str): URL to Arr instance
            api_key (str): API key for Arr instance
            ver_uri (str, optional): API Version. Defaults to "/".
        """

        self.ver_uri = ver_uri
        super().__init__(host_url, api_key)

    # CALENDAR

    # GET /calendar/
    def get_calendar(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        unmonitored: bool = True,
    ) -> JsonArray:
        """Gets upcoming releases by monitored, if start/end are not
        supplied, today and tomorrow will be returned

        Args:
            start_date (Optional[str], optional): ISO8601 start datetime. Defaults to None.
            end_date (Optional[str], optional): ISO8601 end datetime. Defaults to None.
            unmonitored (bool, optional): Include unmonitored movies. Defaults to True.

        Returns:
            JsonArray: List of dictionaries with items
        """
        params: dict[str, Any] = {}
        if start_date:
            params["start"] = start_date.strftime("%Y-%m-%d")
        if end_date:
            params["end"] = end_date.strftime("%Y-%m-%d")
        params["unmonitored"] = unmonitored

        return self._get("calendar", self.ver_uri, params)

    # SYSTEM

    # GET /system/status
    def get_system_status(self) -> JsonObject:
        """Gets system status

        Returns:
           JsonObject: Dictionary with items
        """
        return self._get("system/status", self.ver_uri)

    # GET /health
    def get_health(self) -> JsonArray:
        """Get health information

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("health", self.ver_uri)

    # GET /metadata
    def get_metadata(self, id_: Optional[int] = None) -> Union[JsonArray, JsonObject]:
        """Get all metadata consumer settings

        Args:
            id_ (Optional[int], optional): ID for specific metadata record

        Returns:
             Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        return self._get(f"metadata{f'/{id_}' if id_ else ''}", self.ver_uri)

    # GET /update
    def get_update(self) -> JsonArray:
        """Will return a list of recent updated

        Returns:
             JsonArray: List of dictionaries with items
        """
        return self._get("update", self.ver_uri)

    # GET /rootfolder
    def get_root_folder(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, JsonObject]:
        """Get list of root folders, free space and any unmappedFolders

        Args:
            id_ (Optional[int], optional): ID of the folder to return. Defaults to None.

        Returns:
             Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        return self._get(f"rootfolder{f'/{id_}' if id_ else ''}", self.ver_uri)

    # DELETE /rootfolder
    def del_root_folder(
        self, id_: int
    ) -> Union[
        Response, JsonObject, dict[Any, Any]
    ]:  # sourcery skip: class-extract-method
        """Delete root folder with specified id

        Args:
            id_ (int): Root folder id from database

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"rootfolder/{id_}", self.ver_uri)

    # GET /diskspace
    def get_disk_space(self) -> JsonArray:
        """Query disk usage information
            System > Status

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("diskspace", self.ver_uri)

    # GET /system/backup
    def get_backup(self) -> JsonArray:
        """Returns the list of available backups

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("system/backup", self.ver_uri)

    # LOGS

    # GET /log
    def get_log(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_key: Optional[PyarrLogSortKey] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
        filter_key: Optional[PyarrLogFilterKey] = None,
        filter_value: Optional[PyarrLogFilterValue] = None,
    ) -> JsonObject:
        """Gets logs from instance

        Args:
            page (Optional[int], optional): Specifiy page to return. Defaults to None.
            page_size (Optional[int], optional): Number of items per page. Defaults to None.
            sort_key (Optional[PyarrLogSortKey], optional): Field to sort by. Defaults to None.
            sort_dir (Optional[PyarrSortDirection], optional): Direction to sort. Defaults to None.
            filter_key (Optional[PyarrFilterKey], optional): Key to filter by. Defaults to None.
            filter_value (Optional[PyarrFilterValue], optional): Value of the filter. Defaults to None.

        Returns:
            JsonObject: List of dictionaries with items
        """
        params: dict[
            str,
            Union[
                int,
                PyarrLogSortKey,
                PyarrSortDirection,
                PyarrLogFilterKey,
                PyarrLogFilterValue,
            ],
        ] = {}
        if page:
            params["page"] = page

        if page_size:
            params["pageSize"] = page_size

        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir  must be used together")

        if filter_key and filter_value:
            params["filterKey"] = filter_key
            params["filterValue"] = filter_value
        elif filter_key or filter_value:
            raise PyarrMissingArgument(
                "filter_key and filter_value  must be used together"
            )

        return self._get("log", self.ver_uri, params)

    # GET /history
    def get_history(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_key: Optional[PyarrHistorySortKey] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
    ) -> JsonObject:
        """Gets history (grabs/failures/completed)

        Args:
            page (Optional[int], optional): Page number to return. Defaults to None.
            page_size (Optional[int], optional): Number of items per page. Defaults to None.
            sort_key (Optional[PyarrSortKey], optional): Field to sort by. Defaults to None.
            sort_dir (Optional[PyarrSortDirection], optional): Direction to sort the items. Defaults to None.

        Returns:
           JsonObject: Dictionary with items
        """
        params: dict[
            str,
            Union[
                int,
                PyarrHistorySortKey,
                PyarrSortDirection,
            ],
        ] = {}

        if page:
            params["page"] = page

        if page_size:
            params["pageSize"] = page_size

        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir  must be used together")

        return self._get("history", self.ver_uri, params)

    # BLOCKLIST

    # GET /blocklist
    def get_blocklist(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_key: Optional[PyarrBlocklistSortKey] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
    ) -> JsonObject:
        """Returns blocked releases.

        Args:
            page (Optional[int], optional): Page number to return. Defaults to None.
            page_size (Optional[int], optional): Number of items per page. Defaults to None.
            sort_key (Optional[PyarrBlocklistSortKey], optional): Field to sort by. Defaults to None.
            sort_dir (Optional[PyarrSortDirection], optional): Direction to sort the items. Defaults to None.

        Returns:
            JsonObject: Dictionary with items
        """
        params: dict[str, Union[int, PyarrBlocklistSortKey, PyarrSortDirection]] = {}

        if page:
            params["page"] = page

        if page_size:
            params["pageSize"] = page_size

        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir  must be used together")

        return self._get("blocklist", self.ver_uri, params)

    # DELETE /blocklist
    def del_blocklist(self, id_: int) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Removes a specific release (the id provided) from the blocklist

        Args:
            id_ (int): Blocklist ID from database

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"blocklist/{id_}", self.ver_uri)

    # DELETE /blocklist/bulk
    def del_blocklist_bulk(
        self, ids: list[int]
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete blocked releases in bulk

        Args:
            ids (list[int]): Blocklists ids that should be deleted

        Returns:
            Response: HTTP Response
        """
        data = {"ids": ids}
        return self._delete("blocklist/bulk", self.ver_uri, data=data)

    # PROFILES

    # GET /qualityprofile/{id}
    def get_quality_profile(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, dict[Any, Any]]:
        """Gets all quality profiles or specific one with id

        Args:
            id_ (Optional[int], optional): Quality profile id from database. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items
        """

        path = f"qualityprofile{f'/{id_}' if id_ else ''}"
        return self._get(path, self.ver_uri)

    # PUT /qualityprofile/{id}
    def upd_quality_profile(self, id_: int, data: JsonObject) -> JsonObject:
        """Update the quality profile data

        Note:
            To be used in conjunction with get_quality_profile()

        Args:
            id_ (int): Profile ID to Update
            data (JsonObject): All parameters to update

        Returns:
            JsonObject: Dictionary of updated record
        """

        return self._put(f"qualityprofile/{id_}", self.ver_uri, data=data)

    # DELETE /qualityprofile
    def del_quality_profile(
        self, id_: int
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Removes a specific quality profile from the blocklist

        Args:
            id_ (int): Quality profile ID from database

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"qualityprofile/{id_}", self.ver_uri)

    # GET /qualitydefinition/{id}
    def get_quality_definition(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, dict[Any, Any]]:
        """Gets all quality definitions or specific one by ID

        Args:
            id_ (Optional[int], optional): Import list database id. Defaults to None.

        Returns:
            Union[JsonArray, dict[Any, Any]]: List of dictionaries with items
        """
        path = f"qualitydefinition/{id_}" if id_ else "qualitydefinition"
        return self._get(path, self.ver_uri)

    # PUT /qualitydefinition/{id}
    def upd_quality_definition(self, id_: int, data: JsonObject) -> JsonObject:
        """Update the quality definitions.

        Note:
            To be used in conjunction with get_quality_definition()

        Args:
            id_ (int): ID of definition to update
            data (JsonObject): All parameters to update

        Returns:
            JsonObject: Dictionary of updated record
        """
        return self._put(f"qualitydefinition/{id_}", self.ver_uri, data=data)

    def get_quality_profile_schema(self) -> JsonArray:
        """Get the schemas for quality profiles

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("qualityprofile/schema", self.ver_uri)

    # INDEXER

    # GET /indexer/schema
    def get_indexer_schema(
        self, implementation: Optional[PyarrIndexerSchema] = None
    ) -> Union[JsonArray, JsonObject]:
        """Get possible indexer connections

        Args:
            implementation (Optional[PyarrIndexerSchema], optional): indexer system

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        response: JsonArray = self._get("indexer/schema", self.ver_uri)
        if implementation:
            if filter_response := [
                item for item in response if item["implementation"] == implementation
            ]:
                response = filter_response
            else:
                raise PyarrRecordNotFound(
                    f"A record with implementation {implementation} was not found"
                )
        return response

    # GET /indexer/{id}
    def get_indexer(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, dict[Any, Any]]:
        """Get all indexers or specific by id

        Args:
            id_ (Optional[int], optional): Database if of indexer to return. Defaults to None.

        Returns:
            Union[JsonArray, dict[Any, Any]]: List of dictionaries with items
        """
        path = f"indexer/{id_}" if id_ else "indexer"
        return self._get(path, self.ver_uri)

    # PUT /indexer/{id}
    def upd_indexer(self, id_: int, data: JsonObject) -> JsonObject:
        """Edit a Indexer by database id

        Note:
            To be used in conjunction with get_indexer()

        Args:
            id_ (int): Indexer database id
            data (JsonObject): Data to be updated within Indexer

        Returns:
            JsonObject: Dictionary of updated record
        """
        return self._put(f"indexer/{id_}", self.ver_uri, data=data)

    # DELETE /indexer
    def del_indexer(self, id_: int) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Removes a specific indexer from the blocklist

        Args:
            id_ (int): indexer id from database

        Returns:
            Response: HTTP Response
        """

        return self._delete(f"indexer/{id_}", self.ver_uri)

    # QUEUE

    # DELETE /queue/{id}
    def del_queue(
        self,
        id_: int,
        remove_from_client: Optional[bool] = None,
        blocklist: Optional[bool] = None,
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Remove an item from the queue and blocklist it

        Args:
            id_ (int): ID of the item to be removed
            remove_from_client (Optional[bool], optional): Remove the item from the client. Defaults to None.
            blocklist (Optional[bool], optional): Add the item to the blocklist. Defaults to None.

        Returns:
            Response: HTTP Response
        """
        params = {}
        if remove_from_client:
            params["removeFromClient"] = remove_from_client
        if blocklist:
            params["blocklist"] = blocklist

        return self._delete(f"queue/{id_}", self.ver_uri, params=params)

    # GET /system/task/{id}
    def get_task(
        self,
        id_: Optional[int] = None,
    ) -> JsonObject:
        """Return a list of tasks, or specify a task ID to return single task

        Args:
            id_ (Optional[int], optional):  ID for task. Defaults to None.

        Returns:
            JsonObject: List of dictionaries with items
        """

        path = f"system/task/{id_}" if id_ else "system/task"
        return self._get(path, self.ver_uri)

    # GET /remotepathmapping
    def get_remote_path_mapping(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, dict[Any, Any]]:
        """Get remote path mappings for downloads Directory

        Args:
            id_ (Optional[int], optional): ID for specific record. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items
        """
        _path = f"remotepathmapping{'' if id_ is None else f'/{id_}'}"
        return self._get(_path, self.ver_uri)

    # TODO: Add Delete remote path mapping
    # TODO: Add update remote path mapping

    # CONFIG

    # GET /config/ui
    def get_config_ui(self) -> JsonObject:
        """Query Radarr for UI configuration

        Returns:
            JsonObject: List of dictionaries with items
        """
        return self._get("config/ui", self.ver_uri)

    # PUT /config/ui
    def upd_config_ui(self, data: JsonObject) -> JsonObject:
        """Edit one or many UI settings and save to to the database

        Args:
            data (JsonObject): Data to be Updated.

        Returns:
            JsonObject: Dictionary with items
        """
        return self._put("config/ui", self.ver_uri, data=data)

    # GET /config/host
    def get_config_host(self) -> JsonObject:
        """Get General/Host settings.

        Returns:
            JsonObject: Dictionaries with items
        """
        return self._get("config/host", self.ver_uri)

    # PUT /config/host
    def upd_config_host(self, data: JsonObject) -> JsonObject:
        """Edit General/Host settings.

        Args:
            data (JsonObject): data to be updated

        Returns:
            JsonObject: Dictionaries with items
        """
        return self._put("config/host", self.ver_uri, data=data)

    # GET /config/naming
    def get_config_naming(self) -> JsonObject:
        """Get Settings for file and folder naming.

        Returns:
            JsonObject: Dictionary with items
        """
        return self._get("config/naming", self.ver_uri)

    # PUT /config/naming
    def upd_config_naming(self, data: JsonObject) -> JsonObject:
        """Edit Settings for file and folder naming.

        Args:
            data (JsonObject): data to be updated

        Returns:
            JsonObject: Dictionary with items
        """
        return self._put("config/naming", self.ver_uri, data=data)

    # GET /config/mediamanagement
    def get_media_management(self) -> JsonObject:
        """Get media management configuration

        Returns:
            JsonObject: Dictionary with items
        """
        return self._get("config/mediamanagement", self.ver_uri)

    # PUT /config/mediamanagement
    def upd_media_management(self, data: JsonObject) -> JsonObject:
        """Get media management configuration

        Note:
            Recommended to use with get_media_management()

        Args:
            data (JsonObject): data to be updated

        Returns:
            JsonObject: Dictionary with items
        """
        return self._put("config/mediamanagement", self.ver_uri, data=data)

    # NOTIFICATIONS

    # GET /notification
    def get_notification(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, dict[Any, Any]]:
        """Get a list of all notification services, or single by ID

        Args:
            id_ (Optional[int], optional): Notification ID. Defaults to None.

        Returns:
            Union[JsonArray, dict[Any, Any]]: List of dictionaries with items
        """
        _path = "" if id_ is None else f"/{id_}"
        return self._get(f"notification{_path}", self.ver_uri)

    # GET /notification/schema
    def get_notification_schema(
        self, implementation: Optional[PyarrNotificationSchema] = None
    ) -> Union[JsonArray, JsonObject]:
        """Get possible notification connections

        Args:
            implementation (Optional[PyarrNotificationSchema], optional): notification system

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        response: JsonArray = self._get("notification/schema", self.ver_uri)
        if implementation:
            if filter_response := [
                item for item in response if item["implementation"] == implementation
            ]:
                response = filter_response
            else:
                raise PyarrRecordNotFound(
                    f"A record with implementation {implementation} was not found"
                )
        return response

    # POST /notification
    def add_notification(self, data: JsonObject) -> JsonObject:
        """Add an import list based on the schema information supplied

        Note:
            Recommended to be used in conjunction with get_notification_schema()

        Args:
            data (JsonObject): dictionary with import list schema and settings

        Returns:
            JsonObject: dictionary of added item
        """
        return self._post("notification", self.ver_uri, data=data)

    # PUT /notification/{id}
    def upd_notification(self, id_: int, data: JsonObject) -> JsonObject:
        """Edit notification by database id

        Args:
            id_ (int): Database id of notification
            data (JsonObject): data that requires updating

        Returns:
            JsonObject: Dictionary of updated record
        """
        return self._put(f"notification/{id_}", self.ver_uri, data=data)

    # DELETE /notification/{id}
    def del_notification(self, id_: int) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete a notification by its database id

        Args:
            id_ (int): Database id of notification.

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"notification/{id_}", self.ver_uri)

    # TAGS

    # GET /tag/{id}
    def get_tag(self, id_: Optional[int] = None) -> Union[JsonArray, JsonObject]:
        """Returns all tags or specific tag by database id

        Args:
            id_ (Optional[int], optional): Database id for tag. Defaults to None.

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        path = f"tag/{id_}" if id_ else "tag"
        return self._get(path, self.ver_uri)

    # GET /tag/detail/{id}
    def get_tag_detail(self, id_: Optional[int] = None) -> Union[JsonArray, JsonObject]:
        """Returns all tags or specific tag by database id with detailed information

        Args:
            id_ (Optional[int], optional): Database id for tag. Defaults to None.

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        path = f"tag/detail/{id_}" if id_ else "tag/detail"
        return self._get(path, self.ver_uri)

    # POST /tag
    def create_tag(self, label: str) -> JsonObject:
        """Adds a new tag

        Args:
            label (str): Tag name / label

        Returns:
            JsonObject: Dictionary of new record
        """
        data = {"label": label}
        return self._post("tag", self.ver_uri, data=data)

    # PUT /tag/{id}
    def upd_tag(self, id_: int, label: str) -> JsonObject:
        """Update an existing tag

        Note:
            You should perform a get_tag() and submit the full body with changes

        Args:
            id_ (int): Database id of tag
            label (str): tag name / label

        Returns:
            JsonObject: Dictionary of updated items
        """
        data = {"id": id_, "label": label}
        return self._put("tag", self.ver_uri, data=data)

    # DELETE /tag/{id}
    def del_tag(self, id_: int) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete the tag with the given ID

        Args:
            id_ (int): Database id of tag

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"tag/{id_}", self.ver_uri)

    # DOWNLOAD CLIENT

    # GET /downloadclient/{id}
    def get_download_client(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, JsonObject]:
        """Get a list of all the download clients or a single client by its database id

        Args:
            id_ (Optional[int], optional): Download client database id. Defaults to None.

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        path = f"downloadclient/{id_}" if id_ else "downloadclient"
        return self._get(path, self.ver_uri)

    # GET /downloadclient/schema
    def get_download_client_schema(
        self, implementation: Optional[PyarrDownloadClientSchema] = None
    ) -> JsonArray:
        """Gets the schemas for the different download Clients

        Args:
            implementation (Optional[PyarrDownloadClientSchema], optional): Client implementation name. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items
        """
        response: JsonArray = self._get("downloadclient/schema", self.ver_uri)
        if implementation:
            if filter_response := [
                item for item in response if item["implementation"] == implementation
            ]:
                response = filter_response
            else:
                raise PyarrRecordNotFound(
                    f"A record with implementation {implementation} was not found"
                )
        return response

    # POST /downloadclient/
    def add_download_client(self, data: JsonObject) -> JsonObject:
        """Add a download client based on the schema information supplied

        Note:
            Recommended to be used in conjunction with get_download_client_schema()

        Args:
            data (JsonObject): dictionary with download client schema and settings

        Returns:
            JsonObject: dictionary of added item
        """
        return self._post("downloadclient", self.ver_uri, data=data)

    # PUT /downloadclient/{id}
    def upd_download_client(self, id_: int, data: JsonObject) -> JsonObject:
        """Edit a downloadclient by database id

        Args:
            id_ (int): Download client database id
            data (JsonObject): data to be updated within download client

        Returns:
            dict[str, v]: dictionary of updated item
        """
        return self._put(f"downloadclient/{id_}", self.ver_uri, data=data)

    # DELETE /downloadclient/{id}
    def del_download_client(
        self, id_: int
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete a download client by database id

        Args:
            id_ (int): download client database id

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"downloadclient/{id_}", self.ver_uri)

    # IMPORT LIST

    # GET /importlist
    def get_import_list(self, id_: Optional[int] = None) -> JsonArray:
        """Query for all lists or a single list by its database id

        Args:
            id_ (Optional[int], optional): Import list database id. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items
        """
        path = f"importlist/{id_}" if id_ else "importlist"
        return self._get(path, self.ver_uri)

    def get_import_list_schema(
        self,
        implementation: Optional[
            Union[PyarrImportListSchema, LidarrImportListSchema]
        ] = None,
    ) -> JsonArray:
        """Gets the schemas for the different import list sources

        Args:
            implementation (Optional[Union[PyarrImportListSchema, LidarrImportListSchema]], optional): Client implementation name. Defaults to None.

        Returns:
            JsonArray: List of dictionaries with items
        """
        response: JsonArray = self._get("importlist/schema", self.ver_uri)
        if implementation:
            if filter_response := [
                item for item in response if item["implementation"] == implementation
            ]:
                response = filter_response
            else:
                raise PyarrRecordNotFound(
                    f"A record with implementation {implementation} was not found"
                )
        return response

    # POST /importlist/
    def add_import_list(self, data: JsonObject) -> JsonObject:
        """Add an import list based on the schema information supplied

        Note:
            Recommended to be used in conjunction with get_import_list_schema()

        Args:
            data (JsonObject): dictionary with import list schema and settings

        Returns:
            JsonObject: dictionary of added item
        """
        return self._post("importlist", self.ver_uri, data=data)

    # PUT /importlist/{id}
    def upd_import_list(self, id_: int, data: JsonObject) -> JsonObject:
        """Edit an importlist

        Args:
            id_ (int): Import list database id
            data (JsonObject): data to be updated within the import list

        Returns:
            JsonObject: Dictionary of updated data
        """
        return self._put(f"importlist/{id_}", self.ver_uri, data=data)

    # DELETE /importlist/{id}
    def del_import_list(self, id_: int) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete an import list

        Args:
            id_ (int): Import list database id

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"importlist/{id_}", self.ver_uri)

    # GET /config/downloadclient
    def get_config_download_client(self) -> JsonObject:
        """Gets download client page configuration

        Returns:
            JsonObject: Dictionary of configuration
        """
        return self._get("config/downloadclient", self.ver_uri)

    def upd_config_download_client(self, data: JsonObject) -> JsonObject:
        """Update download client page configurations

        Note:
            Recommended to be used in conjunction with get_config_download_client()

        Args:
            data (JsonObject): data to be updated

        Returns:
            JsonObject: dictionary with updated items
        """
        return self._put("config/downloadclient", self.ver_uri, data=data)

    # GET /command
    def get_command(self, id_: Optional[int] = None) -> Union[JsonArray, JsonObject]:
        """Queries the status of a previously started command, or all currently started commands.

        Args:
            id_ (Optional[int], optional): Database ID of the command. Defaults to None.

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        path = f"command{f'/{id_}' if id_ else ''}"
        return self._get(path, self.ver_uri)

    # GET /language/{id}
    # TODO: update notes and tests for Sonarr once resolved
    def get_language(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, dict[Any, Any]]:
        """Gets all language profiles or specific one with id

        Note:
            This method is not working in Sonarr, use get_language_profile()
            I have raised this with the Sonarr team.

        Args:
            id_ (Optional[int], optional): Language profile id from database. Defaults to None.

        Returns:
            Union[JsonArray, dict[Any, Any]]: List of dictionaries with items
        """

        path = f"language{f'/{id_}' if id_ else ''}"
        return self._get(path, self.ver_uri)
