from datetime import datetime
from typing import Any, Union

from requests import Response

from .const import PAGE, PAGE_SIZE
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
        start_date: Union[str, None] = None,
        end_date: Union[str, None] = None,
        unmonitored: bool = True,
    ) -> list[dict[str, Any]]:
        """Gets upcoming releases by monitored, if start/end are not
        supplied, today and tomorrow will be returned

        Args:
            start_date (Union[str, None], optional): ISO8601 start datetime. Defaults to None.
            end_date (Union[str, None], optional): ISO8601 end datetime. Defaults to None.
            unmonitored (bool, optional): Include unmonitored movies. Defaults to True.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = "calendar"
        params: dict[str, Any] = {}
        if start_date:
            params["start"] = datetime.strptime(start_date, "%Y-%m-%d").strftime(
                "%Y-%m-%d"
            )
        if end_date:
            params["end"] = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        params["unmonitored"] = unmonitored

        response = self._get(path, self.ver_uri, params=params)
        assert isinstance(response, list)
        return response

    # SYSTEM

    # GET /system/status
    def get_system_status(self) -> list[dict[str, Any]]:
        """Gets system status

        Returns:
           list[dict[str, Any]]: List of dictionaries with items
        """
        path = "system/status"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # GET /health
    def get_health(self) -> list[dict[str, Any]]:
        """Get health information

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = "health"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # GET /metadata
    def get_metadata(self) -> list[dict[str, Any]]:
        """Get all metadata consumer settings

        Returns:
             list[dict[str, Any]]: List of dictionaries with items
        """
        path = "metadata"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # GET /update
    def get_update(self) -> list[dict[str, Any]]:
        """Will return a list of recent updated

        Returns:
             list[dict[str, Any]]: List of dictionaries with items
        """
        path = "update"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # GET /rootfolder
    def get_root_folder(self) -> list[dict[str, Any]]:
        """Get list of root folders, free space and any unmappedFolders

        Returns:
             list[dict[str, Any]]: List of dictionaries with items
        """
        path = "rootfolder"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # DELETE /rootfolder
    def del_root_folder(
        self, id_: int
    ) -> Response:  # sourcery skip: class-extract-method
        """Delete root folder with specified id

        Args:
            id_ (int): Root folder id from database

        Returns:
            Response: HTTP Response
        """
        params = {"id": id_}
        path = "rootfolder"
        return self._delete(path, self.ver_uri, params=params)

    # GET /diskspace
    def get_disk_space(self) -> list[dict[str, Any]]:
        """Query disk usage information
            System > Status

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = "diskspace"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # GET /system/backup
    def get_backup(self) -> list[dict[str, Any]]:
        """Returns the list of available backups

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = "system/backup"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # LOGS

    # GET /log
    def get_log(
        self,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_key: str = "time",
        sort_dir: str = "desc",
        filter_key: Union[str, None] = None,
        filter_value: str = "All",
    ) -> list[dict[str, Any]]:
        """Gets logs from instance

        Args:
            page (int, optional): Specifiy page to return. Defaults to PAGE.
            page_size (int, optional): Number of items per page. Defaults to PAGE_SIZE.
            sort_key (str, optional): Field to sort by. Defaults to "time".
            sort_dir (str, optional): Direction to sort. Defaults to "desc".
            filter_key (Union[str, None], optional): Key to filter by. Defaults to None.
            filter_value (str, optional): Value of the filter. Defaults to "All".

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortKey": sort_key,
            "sortDir": sort_dir,
            "filterKey": filter_key,
            "filterValue": filter_value,
        }
        response = self._get("log", self.ver_uri, params=params)
        assert isinstance(response, list)
        return response

    # GET /history
    # TODO: check the ID on this method may need to move to specific APIs
    def get_history(
        self,
        sort_key: str = "date",
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_dir: str = "desc",
        id_: Union[int, None] = None,
    ) -> list[dict[str, Any]]:
        """Gets history (grabs/failures/completed)

        Args:
            sort_key (str, optional): Field to sort by. Defaults to "date".
            page (int, optional): Page number to return. Defaults to PAGE.
            page_size (int, optional): Number of items per page. Defaults to PAGE_SIZE.
            sort_dir (str, optional): Direction to sort the items. Defaults to "desc".
            id_ (Union[int, None], optional): Filter to a specific episode ID. Defaults to None.

        Returns:
           list[dict[str, Any]]: List of dictionaries with items
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
        response = self._get(path, self.ver_uri, params=params)
        assert isinstance(response, list)
        return response

    # BLOCKLIST

    # GET /blocklist
    def get_blocklist(
        self,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_direction: str = "descending",
        sort_key: str = "date",
    ) -> list[dict[str, Any]]:
        """Returns blocked releases.

        Args:
            page (int, optional): Page to be returned. Defaults to PAGE.
            page_size (int, optional): Number of results per page. Defaults to PAGE_SIZE.
            sort_direction (str, optional): Direction to sort items. Defaults to "descending".
            sort_key (str, optional): Field to sort by. Defaults to "date".

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {
            "page": page,
            "pageSize": page_size,
            "sortDirection": sort_direction,
            "sortKey": sort_key,
        }
        path = "blocklist"
        response = self._get(path, self.ver_uri, params=params)
        assert isinstance(response, list)
        return response

    # DELETE /blocklist
    def del_blocklist(self, id_: int) -> Response:
        """Removes a specific release (the id provided) from the blocklist

        Args:
            id_ (int): Blocklist ID from database

        Returns:
            Response: HTTP Response
        """
        params = {"id": id_}
        path = "blocklist"
        return self._delete(path, self.ver_uri, params=params)

    # DELETE /blocklist/bulk
    def del_blocklist_bulk(self, data: dict[str, Any]) -> Response:
        """Delete blocked releases in bulk

        Args:
            data (dict[str, Any]): Blocklists that should be deleted

        Returns:
            Response: HTTP Response
        """
        path = "blocklist/bulk"
        return self._delete(path, self.ver_uri, data=data)

    # PROFILES

    # GET /qualityprofile/{id}
    def get_quality_profile(self, id_: Union[int, None] = None) -> list[dict[str, Any]]:
        """Gets all quality profiles or specific one with id_

        Args:
            id_ (Union[int, None], optional): Quality profile id from database. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"qualityprofile/{id_}" if id_ else "qualityprofile"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # PUT /qualityprofile/{id}
    def upd_quality_profile(self, id_: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update the quality profile data

        Note:
            To be used in conjunction with get_quality_profile()

        Args:
            id_ (int): Profile ID to Update
            data (dict[str, Any]): All parameters to update

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        path = f"qualityprofile/{id_}"
        return self._put(path, self.ver_uri, data=data)

    # DELETE /qualityprofile
    def del_quality_profile(self, id_: int) -> Response:
        """Removes a specific quality profile from the blocklist

        Args:
            id_ (int): Quality profile ID from database

        Returns:
            Response: HTTP Response
        """
        params = {"id": id_}
        path = "qualityprofile"
        return self._delete(path, self.ver_uri, params=params)

    # GET /qualitydefinition/{id}
    def get_quality_definition(
        self, id_: Union[int, None] = None
    ) -> list[dict[str, Any]]:
        """Gets all quality definitions or specific one by ID

        Args:
            id_ (Union[int, None], optional): Import list database id. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"qualitydefinition/{id_}" if id_ else "qualitydefinition"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # PUT /qualitydefinition/{id}
    def upd_quality_definition(self, id_: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update the quality definitions.

        Note:
            To be used in conjunction with get_quality_definition()

        Args:
            id_ (int): ID of definition to update
            data (dict[str, Any]): All parameters to update

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        path = f"qualitydefinition/{id_}"
        return self._put(path, self.ver_uri, data=data)

    # INDEXER

    # GET /indexer/{id}
    def get_indexer(self, id_: Union[int, None] = None) -> list[dict[str, Any]]:
        """Get all indexers or specific by id

        Args:
            id_ (Union[int, None], optional): Database if of indexer to return. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"indexer/{id_}" if id_ else "indexer"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # PUT /indexer/{id}
    def upd_indexer(self, id_: int, data: dict[str, Any]) -> dict[str, Any]:
        """Edit a Indexer by database id

        Note:
            To be used in conjunction with get_indexer()

        Args:
            id_ (int): Indexer database id
            data (dict[str, Any]): Data to be updated within Indexer

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        path = f"indexer/{id_}"
        return self._put(path, self.ver_uri, data=data)

    # DELETE /indexer
    def del_indexer(self, id_: int) -> Response:
        """Removes a specific indexer from the blocklist

        Args:
            id_ (int): indexer id from database

        Returns:
            Response: HTTP Response
        """
        params = {"id": id_}
        path = "indexer"
        return self._delete(path, self.ver_uri, params=params)

    # QUEUE

    # DELETE /queue/{id}
    def del_queue(
        self, id_: int, remove_from_client: bool = True, blacklist: bool = True
    ) -> Response:
        """Remove an item from the queue and blacklist it

        Args:
            id_ (int): ID of the item to be removed
            remove_from_client (bool, optional): Remove the item from the client. Defaults to True.
            blacklist (bool, optional): Add the item to the blacklist. Defaults to True.

        Returns:
            Response: HTTP Response
        """
        params = {"removeFromClient": remove_from_client, "blacklist": blacklist}
        path = f"queue/{id_}"
        return self._delete(path, self.ver_uri, params=params)

    # GET /system/task/{id}
    def get_task(self, id_: Union[int, None] = None) -> list[dict[str, Any]]:
        """Return a list of tasks, or specify a task ID to return single task

        Args:
            id_ (Union[int, None], optional):  ID for task. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"system/task/{id_}" if id_ else "system/task"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # GET /remotepathmapping
    def get_remote_path_mapping(
        self, id_: Union[int, None] = None
    ) -> list[dict[str, Any]]:
        """Get remote path mappings for downloads Directory

        Args:
            id_ (Union[int, None], optional): ID for specific record. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        _path = "" if isinstance(id_, str) or id_ is None else f"/{id_}"
        response = self._get(f"remotepathmapping{_path}", self.ver_uri)
        assert isinstance(response, list)
        return response

    # CONFIG

    # GET /config/ui
    def get_config_ui(self) -> dict[str, Any]:
        """Query Radarr for UI configuration

        Returns:
            dict[str, Any]: List of dictionaries with items
        """
        path = "config/ui"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, dict)
        return response

    # PUT /config/ui
    def upd_config_ui(self, data: dict[str, Any]) -> dict[str, Any]:
        """Edit one or many UI settings and save to to the database

        Args:
            data (dict[str, Any]): Data to be Updated.

        Returns:
            dict[str, Any]: Dictionary with items
        """
        path = "config/ui"
        return self._put(path, self.ver_uri, data=data)

    # GET /config/host
    def get_config_host(self) -> dict[str, Any]:
        """Get General/Host settings.

        Returns:
            dict[str, Any]: Dictionaries with items
        """
        path = "config/host"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, dict)
        return response

    # PUT /config/host
    def upd_config_host(self, data: dict[str, Any]) -> dict[str, Any]:
        """Edit General/Host settings.

        Args:
            data (dict[str, Any]): data to be updated

        Returns:
            dict[str, Any]: Dictionaries with items
        """
        path = "config/host"
        return self._put(path, self.ver_uri, data=data)

    # GET /config/naming
    def get_config_naming(self) -> dict[str, Any]:
        """Get Settings for file and folder naming.

        Returns:
            dict[str, Any]: Dictionary with items
        """
        path = "config/naming"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, dict)
        return response

    # PUT /config/naming
    def upd_config_naming(self, data: dict[str, Any]) -> dict[str, Any]:
        """Edit Settings for file and folder naming.

        Args:
            data (dict[str, Any]): data to be updated

        Returns:
            dict[str, Any]: Dictionary with items
        """
        path = "config/naming"
        return self._put(path, self.ver_uri, data=data)

    # GET /config/mediamanagement
    def get_media_management(self) -> dict[str, Any]:
        """Get media management configuration

        Returns:
            dict[str, Any]: Dictionary with items
        """
        path = "config/mediamanagement"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, dict)
        return response

    # PUT /config/mediamanagement
    def upd_media_management(self, data: dict[str, Any]) -> dict[str, Any]:
        """Get media management configuration

        Note:
            Recommended to use with get_media_management()

        Args:
            data (dict[str, Any]): data to be updated

        Returns:
            dict[str, Any]: Dictionary with items
        """
        return self._put("config/mediamanagement", self.ver_uri, data=data)

    # NOTIFICATIONS

    # GET /notification
    def get_notification(self, id_: Union[int, None] = None) -> list[dict[str, Any]]:
        """Get a list of all notification services, or single by ID

        Args:
            id_ (Union[int, None], optional): Notification ID. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        _path = "" if isinstance(id_, str) or id_ is None else f"/{id_}"
        response = self._get(f"notification{_path}", self.ver_uri)
        assert isinstance(response, list)
        return response

    # GET /notification/schema
    def get_notification_schema(self) -> list[dict[str, Any]]:
        """Get possible notification connections

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = "notification/schema"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # PUT /notification/{id}
    def upd_notification(self, id_: int, data: dict[str, Any]) -> dict[str, Any]:
        """Edit notification by database id

        Args:
            id_ (int): Database id of notification
            data (dict[str, Any]): data that requires updating

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        return self._put(f"notification/{id_}", self.ver_uri, data=data)

    # DELETE /notification/{id}
    def del_notification(self, id_: int) -> Response:
        """Delete a notification by its database id

        Args:
            id_ (int): Database id of notification.

        Returns:
            Response: HTTP Response
        """
        path = f"notification/{id_}"
        return self._delete(path, self.ver_uri)

    # TAGS

    # GET /tag/{id}
    def get_tag(self, id_: Union[int, None] = None) -> list[dict[str, Any]]:
        """Returns all tags or specific tag by database id

        Args:
            id_ (Union[int, None], optional): Database id for tag. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"tag/{id_}" if id_ else "tag"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # GET /tag/detail/{id}
    def get_tag_detail(self, id_: Union[int, None] = None) -> list[dict[str, Any]]:
        """Returns all tags or specific tag by database id with detailed information

        Args:
            id_ (Union[int, None], optional): Database id for tag. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"tag/detail/{id_}" if id_ else "tag/detail"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # POST /tag
    def create_tag(self, label: str) -> dict[str, Any]:
        """Adds a new tag

        Args:
            label (str): Tag name / label

        Returns:
            dict[str, Any]: Dictionary of new record
        """
        data = {"label": label}
        path = "tag"
        return self._post(path, self.ver_uri, data=data)

    # PUT /tag/{id}
    def upd_tag(self, id_: int, label: str) -> dict[str, Any]:
        """Update an existing tag

        Note:
            You should perform a get_tag() and submit the full body with changes

        Args:
            id_ (int): Database id of tag
            label (str): tag name / label

        Returns:
            dict[str, Any]: Dictionary of updated items
        """
        data = {"id": id_, "label": label}
        path = f"tag/{id_}"
        return self._put(path, self.ver_uri, data=data)

    # DELETE /tag/{id}
    def del_tag(self, id_: int) -> Response:
        """Delete the tag with the given ID

        Args:
            id_ (int): Database id of tag

        Returns:
            Response: HTTP Response
        """
        path = f"tag/{id_}"
        return self._delete(path, self.ver_uri)

    # DOWNLOAD CLIENT

    # GET /downloadclient/{id}
    def get_download_client(self, id_: Union[int, None] = None) -> list[dict[str, Any]]:
        """Get a list of all the download clients or a single client by its database id

        Args:
            id_ (Union[int, None], optional): Download client database id. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"downloadclient/{id_}" if id_ else "downloadclient"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # GET /downloadclient/schema
    def get_download_client_schema(
        self, implementation_: Union[str, None] = None
    ) -> list[dict[str, Any]]:
        """Gets the schemas for the different download Clients

        Args:
            implementation_ (Union[str, None], optional): Client implementation name. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        response = self._get("downloadclient/schema", self.ver_uri)
        assert isinstance(response, list)
        if implementation_:
            return [
                schema
                for schema in response
                if schema["implementation"] == implementation_
            ]

        return response

    # POST /downloadclient/
    def add_download_client(self, data: dict[str, Any]) -> dict[str, Any]:
        """Add a download client based on the schema information supplied

        Note:
            Recommended to be used in conjunction with get_download_client_schema()

        Args:
            data (dict[str, Any]): dictionary with download client schema and settings

        Returns:
            dict[str, Any]: dictionary of added item
        """
        return self._post("downloadclient", self.ver_uri, data=data)

    # PUT /downloadclient/{id}
    def upd_download_client(self, id_: int, data: dict[str, Any]) -> dict[str, Any]:
        """Edit a downloadclient by database id

        Args:
            id_ (int): Download client database id
            data (dict[str, Any]): data to be updated within download client

        Returns:
            dict[str, Any]: dictionary of updated item
        """
        path = f"downloadclient/{id_}"
        return self._put(path, self.ver_uri, data=data)

    # DELETE /downloadclient/{id}
    def del_download_client(self, id_: int) -> Response:
        """Delete a download client by database id

        Args:
            id_ (int): download client database id

        Returns:
            Response: HTTP Response
        """
        path = f"downloadclient/{id_}"
        return self._delete(path, self.ver_uri)

    # IMPORT LIST

    # GET /importlist
    def get_import_list(self, id_: Union[int, None] = None) -> list[dict[str, Any]]:
        """Query for all lists or a single list by its database id

        Args:
            id_ (Union[int, None], optional): Import list database id. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"importlist/{id_}" if id_ else "importlist"
        response = self._get(path, self.ver_uri)
        assert isinstance(response, list)
        return response

    # POST /importlist/
    def add_import_list(self) -> Any:
        """This is not implemented yet

        Raises:
            NotImplementedError: Error
        """
        raise NotImplementedError()

    # PUT /importlist/{id}
    def upd_import_list(self, id_: int, data: dict[str, Any]) -> dict[str, Any]:
        """Edit an importlist

        Args:
            id_ (int): Import list database id
            data (dict[str, Any]): data to be updated within the import list

        Returns:
            dict[str, Any]: Dictionary of updated data
        """
        path = f"importlist/{id_}"
        return self._put(path, self.ver_uri, data=data)

    # DELETE /importlist/{id}
    def del_import_list(self, id_: int) -> Response:
        """Delete an import list

        Args:
            id_ (int): Import list database id

        Returns:
            Response: HTTP Response
        """
        return self._delete(f"importlist/{id_}", self.ver_uri)

    # GET /config/downloadclient
    def get_config_download_client(self) -> dict[str, Any]:
        """Gets download client page configuration

        Returns:
            dict[str, Any]: Dictionary of configuration
        """
        response = self._get("config/downloadclient", self.ver_uri)
        assert isinstance(response, dict)
        return response

    # POST /notifications
    def add_notifications(self) -> Any:
        """This is not implemented yet

        Raises:
            NotImplementedError: Error
        """
        raise NotImplementedError()
