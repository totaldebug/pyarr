from typing import Any, Optional, Union

from requests import Response

from pyarr.types import JsonArray, JsonObject

from .base import BaseArrAPI
from .exceptions import PyarrMissingArgument, PyarrMissingProfile
from .models.common import PyarrSortDirection
from .models.readarr import ReadarrAuthorMonitor, ReadarrCommands, ReadarrSortKeys


class ReadarrAPI(BaseArrAPI):
    """API wrapper for Readarr endpoints."""

    def __init__(self, host_url: str, api_key: str):
        """Initialise Readarr API

        Args:
            host_url (str): URL for Readarr
            api_key (str): API key for Readarr
        """

        ver_uri = "/v1"
        super().__init__(host_url, api_key, ver_uri)

    def lookup(self, term: str) -> JsonArray:
        """Search for an author / book by name or Goodreads ID / ISBN / ASIN

        Note:
            You can also search using the Goodreads ID, work, or author, the ISBN or ASIN::

                readarr.lookup(term="edition:656")
                readarr.lookup(term="work:4912789")
                readarr.lookup(term="author:128382")
                readarr.lookup(term="isbn:067003469X")
                readarr.lookup(term="asin:B00JCDK5ME")

        Args:
            term (str): Search term

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("search", self.ver_uri, params={"term": term})

    # GET /book/lookup
    def lookup_book(self, term: str) -> JsonArray:
        """Searches for new books using a term, goodreads ID, isbn or asin.

        Args:
            term (str): Search term::

                goodreads:656
                isbn:067003469X
                asin:B00JCDK5ME

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("book/lookup", self.ver_uri, {"term": term})

    # GET /author/lookup/
    def lookup_author(self, term: str) -> JsonArray:
        """Searches for new authors using a term

        Args:
            term (str): Author name or book

        Returns:
            JsonArray: List of dictionaries with items
        """
        params = {"term": term}
        return self._get("author/lookup", self.ver_uri, params)

    # COMMAND

    # GET /command/:id
    def get_command(self, id_: Optional[int] = None) -> Union[JsonArray, JsonObject]:
        """Queries the status of a previously started command, or all currently started commands.

        Args:
            id_ (Optional[int], optional): Database ID of the command. Defaults to None.

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        path = f"command/{id_}" if id_ else "command"
        return self._get(path, self.ver_uri)

    # POST /command
    def post_command(
        self,
        name: ReadarrCommands,
        **kwargs: Optional[dict[str, Union[int, list[int]]]],
    ) -> JsonObject:
        """Performs any of the predetermined Readarr command routines

        Args:
            name (ReadarrCommands): Command name that should be executed
            **kwargs: Additional parameters for specific commands

        Note:
            For available commands and required `**kwargs` see the `ReadarrCommands` model


        Returns:
            JsonObject: Dictionary of command run
        """
        data: dict[str, Any] = {
            "name": name,
        }
        if kwargs:
            data |= kwargs
        return self._post("command", self.ver_uri, data=data)

    ## WANTED (MISSING)

    # GET /wanted/missing
    def get_missing(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_key: Optional[ReadarrSortKeys] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
    ) -> JsonObject:
        """Gets missing episode (episodes without files)

        Args:
            page (int, optional): Page number to return. Defaults to None.
            page_size (int, optional): Number of items per page. Defaults to None.
            sort_key (ReadarrSortKeys, optional): id, title, ratings, bookid, or quality. (Others do not apply). Defaults to None.
            sort_dir (PyarrSortDirection, optional): Direction to sort the items. Defaults to None,

        Returns:
            JsonObject: List of dictionaries with items
        """
        params: dict[str, Union[int, ReadarrSortKeys, PyarrSortDirection, bool]] = {}
        if page:
            params["page"] = page
        if page_size:
            params["pageSize"] = page_size
        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir  must be used together")
        return self._get("wanted/missing", self.ver_uri, params)

    # GET /wanted/cutoff
    def get_cutoff(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_key: Optional[ReadarrSortKeys] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
        monitored: bool = None,
    ) -> JsonObject:
        """Get wanted items where the cutoff is unmet

        Args:
            page (int, optional): Page number to return. Defaults to None.
            page_size (int, optional):  Number of items per page. Defaults to None.
            sort_key (ReadarrSortKeys, optional): id, title, ratings, bookid, or quality". (others do not apply). Defaults to None.
            sort_dir (PyarrSortDirection, optional): Direction to sort. Defaults to None.
            monitored (bool, optional): Search for monitored only. Defaults to None.

        Returns:
            JsonObject: List of dictionaries with items
        """
        params: dict[str, Union[int, ReadarrSortKeys, PyarrSortDirection, bool]] = {}
        if page:
            params["page"] = page
        if page_size:
            params["pageSize"] = page_size
        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir  must be used together")
        if monitored:
            params["monitored"] = monitored
        return self._get("wanted/cutoff", self.ver_uri, params)

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_key: Optional[ReadarrSortKeys] = None,
        sort_dir: Optional[PyarrSortDirection] = None,
        unknown_authors: Optional[bool] = None,
        include_author: Optional[bool] = None,
        include_book: Optional[bool] = None,
    ) -> JsonObject:
        """Get current download information

        Args:
            page (int, optional): Page number. Defaults to None.
            page_size (int, optional): Number of items per page. Defaults to None.
            sort_key (ReadarrSortKeys, optional): Field to sort by. Defaults to None.
            sort_dir (PyarrSortDirection, optional): Direction to sort. Defaults to None.
            unknown_authors (bool, optional): Include items with an unknown author. Defaults to None.
            include_author (bool, optional): Include the author. Defaults to None.
            include_book (bool, optional): Include the book. Defaults to None.

        Returns:
            JsonObject: List of dictionaries with items
        """
        params: dict[str, Union[int, ReadarrSortKeys, PyarrSortDirection, bool]] = {}
        if page:
            params["page"] = page
        if page_size:
            params["pageSize"] = page_size
        if sort_key and sort_dir:
            params["sortKey"] = sort_key
            params["sortDirection"] = sort_dir
        elif sort_key or sort_dir:
            raise PyarrMissingArgument("sort_key and sort_dir  must be used together")
        if unknown_authors:
            params["includeUnknownAuthorItems"] = unknown_authors
        if include_author:
            params["includeAuthor"] = include_author
        if include_book:
            params["includeBook"] = include_book

        return self._get("queue", self.ver_uri, params)

    # PROFILES

    # POST /qualityprofile
    def add_quality_profile(self, name: str, upgrades_allowed: bool, cutoff: int, items: list, min_format_score: int = 0, cutoff_format_score: int = 0, format_items: list = None) -> JsonObject:  # type: ignore[override]
        """Add new quality profile

        Args:
            name (str): Name of the profile
            upgrades_allowed (bool): Are upgrades in quality allowed?
            cutoff (int): ID of quality definition to cutoff at. Must be an allowed definition ID.
            items (list): Add a list of items (from `get_quality_definition()`)
            min_format_score (int): minimum score for format. Defaults to 0
            cutoff_format_score (int): cutoff format score. Defaults to 0
            format_items (list): custom format items. Defaults to []

        Returns:
            JsonObject: An object containing the profile
        """
        if format_items is None:
            format_items = []
        data = {
            "name": name,
            "upgradeAllowed": upgrades_allowed,
            "cutoff": cutoff,
            "items": items,
            "minFormatScore": min_format_score,
            "cutoffFormatScore": cutoff_format_score,
            "formatItems": format_items,
        }
        return self._post("qualityprofile", self.ver_uri, data=data)

    # GET /metadataprofile/{id}
    def get_metadata_profile(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, dict[Any, Any]]:
        """Gets all metadata profiles or specific one with ID

        Args:
            id_ (Optional[int], optional): Metadata profile id from database. Defaults to None.

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        path = f"metadataprofile/{id_}" if id_ else "metadataprofile"
        return self._get(path, self.ver_uri)

    # POST /metadataprofile
    def add_metadata_profile(
        self,
        name: str,
        min_popularity: int,
        skip_missing_date: bool,
        skip_missing_isbn: bool,
        skip_parts_and_sets: bool,
        skip_series_secondary: bool,
        allowed_languages: str,
        min_pages: int,
    ) -> Union[JsonArray, JsonObject]:
        """Add a metadata profile

        Args:
            name (str): Name of the profile
            min_popularity (int): Minimum popularity
            skip_missing_date (bool): Skip missing dates
            skip_missing_isbn (bool): Skip missing isbn
            skip_parts_and_sets (bool): Skip parts and sets
            skip_series_secondary (bool): Skip series secondary
            allowed_languages (str): List of allowed languages
            min_pages (int): minimum pages

        Returns:
            Union[JsonArray, JsonObject]: object of added record
        """
        data = {
            "name": name,
            "minPopularity": min_popularity,
            "skipMissingDate": skip_missing_date,
            "skipMissingIsbn": skip_missing_isbn,
            "skipPartsAndSets": skip_parts_and_sets,
            "skipSeriesSecondary": skip_series_secondary,
            "allowedLanguages": allowed_languages,
            "minPages": min_pages,
        }
        return self._post("metadataprofile", self.ver_uri, data=data)

    # DELETE /metadataprofile/{id}
    def del_metadata_profile(
        self,
        id_: int,
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete the metadata profile with the given ID

        Args:
            id_ (int): Database ID for metadata profile

        Returns:
            Response: HTTP Response
        """

        return self._delete(f"metadataprofile/{id_}", self.ver_uri)

    # GET /delayprofile/{id}
    def get_delay_profile(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, JsonObject]:
        """Gets all delay profiles or specific one with ID

        Args:
            id_ (Optional[int], optional): Metadata profile ID from database. Defaults to None.

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        path = f"delayprofile/{id_}" if id_ else "delayprofile"
        return self._get(path, self.ver_uri)

    # GET /releaseprofile/{id}
    def get_release_profile(
        self, id_: Optional[int] = None
    ) -> Union[JsonArray, JsonObject]:
        """Gets all release profiles or specific one with ID

        Args:
            id_ (Optional[int], optional): Release profile ID from database. Defaults to None.

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        path = f"releaseprofile/{id_}" if id_ else "releaseprofile"
        return self._get(path, self.ver_uri)

    ## BOOKS

    # GET /book and /book/{id}
    def get_book(self, id_: Optional[int] = None) -> Union[JsonArray, JsonObject]:
        """Returns all books in your collection or the book with the matching
        book ID if one is found.

        Args:
            id_ (Optional[int], optional): Database id for book. Defaults to None.

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        path = f"book/{id_}" if id_ else "book"
        return self._get(path, self.ver_uri)

    # POST /book
    def add_book(
        self,
        book: JsonObject,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        search_for_new_book: bool = False,
        author_monitor: ReadarrAuthorMonitor = "all",
        author_search_for_missing_books: bool = False,
    ) -> JsonObject:
        """Add a new book and its associated author (if not already added).

        Args:
            book (JsonObject): A book object from `lookup()`
            root_dir (str): The root directory for the books to be saved.
            quality_profile_id (Optional[int], optional): Quality Profile. Defaults to first found profile.
            metadata_profile_id (Optional[int], optional): Metadata Profile. Defaults to first found profile.
            monitored (bool, optional): Monitor the book. Defaults to True.
            search_for_new_book (bool, optional): Look for new books. Defaults to False.
            author_monitor (ReadarrAuthorMonitor, optional): Monitor the author for books. Defaults to "all".
            author_search_for_missing_books (bool, optional): Search missing books by the author. Defaults to False.

        Returns:
            JsonObject: A copy of the added books
        """
        if quality_profile_id is None:
            try:
                quality_profile_id = self.get_quality_profile()[0]["id"]
            except IndexError as exception:
                raise PyarrMissingProfile(
                    "There is no Quality Profile setup"
                ) from exception
        if metadata_profile_id is None:
            try:
                metadata_profile_id = self.get_metadata_profile()[0]["id"]
            except IndexError as exception:
                raise PyarrMissingProfile(
                    "There is no Metadata Profile setup"
                ) from exception

        book["author"]["rootFolderPath"] = root_dir
        book["author"]["metadataProfileId"] = metadata_profile_id
        book["author"]["qualityProfileId"] = quality_profile_id
        book["author"]["rootFolderPath"] = root_dir
        book["author"]["addOptions"] = {
            "monitor": author_monitor,
            "searchForMissingBooks": author_search_for_missing_books,
        }
        book["monitored"] = monitored
        book["author"]["manualAdd"] = True
        book["addOptions"] = {"searchForNewBook": search_for_new_book}

        return self._post("book", self.ver_uri, data=book)

    # PUT /book/{id}
    def upd_book(self, book: JsonObject, editions: JsonArray) -> JsonObject:
        """Update the given book.

        Note:
            To be used in conjunction with get_book() and get_edition()

            Currently only monitored states are updated (for the book and edition).

        Args:
            id_ (int): Book database ID to update
            book (JsonObject): All parameters to update book
            editions (JsonArray): List of editions to update book from `get_edition()`

        Returns:
            JsonObject: Dictionary with updated record
        """
        book["editions"] = editions

        return self._put("book", self.ver_uri, data=book)

    # PUT /book/monitor
    def upd_book_monitor(
        self, book_ids: list[int], monitored: bool = True
    ) -> JsonArray:
        """Update book monitored status

        Args:
            book_ids (list[int]): All book IDs to be updated
            monitored (bool, optional): True or False. Defaults to True.

        Returns:
            JsonArray: list of dictionaries containing updated records
        """
        return self._put(
            "book/monitor",
            self.ver_uri,
            data={"bookIds": book_ids, "monitored": monitored},
        )

    # DELETE /book/{id}
    def del_book(
        self,
        id_: int,
        delete_files: Optional[bool] = None,
        import_list_exclusion: Optional[bool] = None,
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete the book with the given ID

        Args:
            id_ (int): Database ID for book
            delete_files (bool, optional): If true book folder and files will be deleted. Defaults to None.
            import_list_exclusion (bool, optional): Add an exclusion so book doesn't get re-added. Defaults to None.

        Returns:
            Response: HTTP Response
        """
        params: dict[str, bool] = {}
        if delete_files:
            params["deleteFiles"] = delete_files
        if import_list_exclusion:
            params["addImportListExclusion"] = import_list_exclusion

        return self._delete(f"book/{id_}", self.ver_uri, params=params)

    # AUTHORadd_author

    # GET /author and /author/{id}
    def get_author(self, id_: Optional[int] = None) -> Union[JsonArray, JsonObject]:
        """Returns all authors in your collection or the author with the matching ID if one is found.

        Args:
            id_ (Optional[int], optional): Database ID for author. Defaults to None.

        Returns:
            Union[JsonArray, JsonObject]: List of dictionaries with items
        """
        path = f"author/{id_}" if id_ else "author"
        return self._get(path, self.ver_uri)

    # POST /author/
    def add_author(
        self,
        author: JsonObject,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        author_monitor: ReadarrAuthorMonitor = "none",
        author_search_for_missing_books: bool = False,
    ) -> JsonObject:
        """Adds an author based on data from lookup, must be an author record

        Args:
            author (JsonObject): A author object from `lookup()`
            root_dir (str): Directory for book to be stored
            quality_profile_id (int, optional): Quality profile id. Defaults to 1.
            metadata_profile_id (int, optional): Metadata profile id. Defaults to 0.
            monitored (bool, optional): Should the author be monitored. Defaults to True.
            author_monitor (ReadarrAuthorMonitor, optional): What level  should the author be monitored. Defaults to "none".
            author_search_for_missing_books (bool, optional): Search for any missing books by the author. Defaults to False.

        Returns:
            JsonObject: Dictonary of added record
        """
        if quality_profile_id is None:
            try:
                quality_profile_id = self.get_quality_profile()[0]["id"]
            except IndexError as exception:
                raise PyarrMissingProfile(
                    "There is no Quality Profile setup"
                ) from exception
        if metadata_profile_id is None:
            try:
                metadata_profile_id = self.get_metadata_profile()[0]["id"]
            except IndexError as exception:
                raise PyarrMissingProfile(
                    "There is no Metadata Profile setup"
                ) from exception
        author["metadataProfileId"] = metadata_profile_id
        author["qualityProfileId"] = quality_profile_id
        author["rootFolderPath"] = root_dir
        author["addOptions"] = {
            "monitor": author_monitor,
            "searchForMissingBooks": author_search_for_missing_books,
        }
        author["monitored"] = monitored
        return self._post("author", self.ver_uri, data=author)

    # PUT /author/{id}
    def upd_author(self, id_: int, data: JsonObject) -> JsonObject:
        """Update the given author, currently only monitored is changed, all other modifications are ignored.

        Note:
            To be used in conjunction with get_author()

        Args:
            id_ (int): Author database ID to update
            data (JsonObject): All parameters to update author

        Returns:
            JsonObject: Dictionary with updated record
        """
        return self._put(f"author/{id_}", self.ver_uri, data=data)

    # DELETE /author/{id}
    def del_author(
        self,
        id_: int,
        delete_files: Optional[bool] = None,
        import_list_exclusion: Optional[bool] = None,
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete the author with the given ID

        Args:
            id_ (int): Database ID for author
            delete_files (bool, optional): If true author folder and files will be deleted. Defaults to None.
            import_list_exclusion (bool, optional): Add an exclusion so author doesn't get re-added. Defaults to None.

        Returns:
            Response: HTTP Response
        """
        params: dict[str, bool] = {}
        if delete_files:
            params["deleteFiles"] = delete_files
        if import_list_exclusion:
            params["addImportListExclusion"] = import_list_exclusion

        return self._delete(f"author/{id_}", self.ver_uri, params=params)

    ## LOG

    # GET /log/file
    def get_log_file(self) -> JsonArray:
        """Get log file

        Returns:
            JsonArray: List of dictionaries with items
        """
        return self._get("log/file", self.ver_uri)

    # CONFIG

    # POST /rootFolder/
    def add_root_folder(
        self,
        name: str,
        path: str,
        default_quality_profile_id: int,
        default_metadata_profile_id: int,
        default_tags: Optional[list] = None,
        is_calibre_lib: bool = False,
        calibre_host: str = "localhost",
        calibre_port: int = 8080,
        use_ssl: bool = False,
        output_profile: str = "default",
    ) -> JsonObject:
        """Add a new location to store files

        Args:
            name (str): Friendly Name for folder
            path (str): Location the files should be stored
            default_quality_profile_id (int): Quality Profile.
            default_metadata_profile_id (int): Metadata Profile.
            default_tags (Optional[list], optional): List of tags to apply. Defaults to None.
            is_calibre_lib (bool, optional): Use Calibre Content Server. Defaults to False.
            calibre_host (str, optional): Calibre Content Server address. Defaults to "localhost".
            calibre_port (int, optional): Calibre Content Server port. Defaults to 8080.
            use_ssl (bool, optional): Calibre Content Server SSL. Defaults to False.
            output_profile (str, optional): Books to monitor. Defaults to "default".

        Returns:
            JsonObject: Dictionary of added record
        """
        folder_json = {
            "isCalibreLibrary": is_calibre_lib,
            "host": calibre_host,
            "port": calibre_port,
            "useSsl": use_ssl,
            "outputProfile": output_profile,
            "defaultTags": default_tags or [],
            "defaultQualityProfileId": default_quality_profile_id,
            "defaultMetadataProfileId": default_metadata_profile_id,
            "name": name,
            "path": path,
        }
        return self._post("rootFolder", self.ver_uri, data=folder_json)

    # GET /config/metadataProvider
    def get_metadata_provider(self) -> JsonObject:
        """Get metadata provider from settings/metadata

        Returns:
            JsonObject: Dictionary of record
        """
        return self._get("config/metadataProvider", self.ver_uri)

    # PUT /config/metadataProvider
    def upd_metadata_provider(self, data: JsonObject) -> JsonObject:
        """Update the metadata provider data.

        Note:
            To be used in conjunction with get_metadata_provider()

        Args:
            data (JsonObject): All parameters to update

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        return self._put("config/metadataProvider", self.ver_uri, data=data)

    def add_release_profile(
        self,
        ignored: list,
        required: list,
        indexerId: int = 0,
        tags: list[int] = None,
        enabled: bool = True,
        includePreferredWhenRenaming: bool = False,
    ) -> JsonObject:
        """Add a Release Profile

        Args:
            ignored (list): List of terms in the release to ignore
            indexerId (int): ID for preferred indexer. Defaults to 0 (any).
            required (list): List of terms the release must include.
            tags (list[int]): List of tag id's. Defaults to empty list
            enabled (bool, optional): Enable release profile. Defaults to True.
            includePreferredWhenRenaming (bool, optional): Include preferred when renaming. Defaults to False.

        Returns:
            JsonObject: Dictionary containing details of new profile
        """

        if tags is None:
            tags = []

        data: dict[str, Any] = {
            "enabled": enabled,
            "ignored": ignored,
            "includePreferredWhenRenaming": includePreferredWhenRenaming,
            "indexerId": indexerId,
            "required": required,
            "tags": tags,
        }
        return self._post(
            "releaseprofile",
            self.ver_uri,
            data=data,
        )

    # DELETE /releaseprofile/{id}
    def del_release_profile(
        self,
        id_: int,
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete the release profile with the given ID

        Args:
            id_ (int): Database ID for release profile

        Returns:
            Response: HTTP Response
        """

        return self._delete(f"releaseprofile/{id_}", self.ver_uri)

    def add_delay_profile(
        self,
        tags: list[int],
        preferredProtocol: str = "usenet",
        usenetDelay: int = 0,
        torrentDelay: int = 0,
        bypassIfHighestQuality: bool = False,
        bypassIfAboveCustomFormatScore: bool = False,
        minimumCustomFormatScore: int = 0,
    ) -> JsonObject:
        """Add delay profile

        Args:
            tags (list[int]): List of tag IDs. Use: `get_tag`.
            preferredProtocol (str, optional): usenet, torrent, onlyusenet, onlytorrent  . Defaults to "usenet".
            usenetDelay (int, optional): Delay before grabbing a release. Defaults to 0.
            torrentDelay (int, optional): Delay before grabbing a release. Defaults to 0.
            bypassIfHighestQuality (bool, optional): Bypass delay when release has the highest enabled quality in the quality profile. Defaults to False.
            bypassIfAboveCustomFormatScore (bool, optional): Enable bypass when release has a score higher than the configured minimum custom format score. Defaults to False.
            minimumCustomFormatScore (int, optional): set when using `bypassIfAboveCustomFormatScore`. Defaults to 0.

        Returns:
            JsonObject: Dictonary with added item
        """
        data = {
            "enableUsenet": True,
            "enableTorrent": True,
            "preferredProtocol": preferredProtocol,
            "usenetDelay": usenetDelay,
            "torrentDelay": torrentDelay,
            "bypassIfHighestQuality": bypassIfHighestQuality,
            "bypassIfAboveCustomFormatScore": bypassIfAboveCustomFormatScore,
            "minimumCustomFormatScore": minimumCustomFormatScore,
            "tags": tags,
        }

        if preferredProtocol == "onlytorrent":
            data["preferredProtocol"] = "torrent"
            data["enableUsenet"] = False
        elif preferredProtocol == "onlyusenet":
            data["preferredProtocol"] = "usenet"
            data["enableTorrent"] = False
        return self._post("delayprofile", self.ver_uri, data=data)

    # DELETE /delayprofile/{id}
    def del_delay_profile(
        self,
        id_: int,
    ) -> Union[Response, JsonObject, dict[Any, Any]]:
        """Delete the delay profile with the given ID

        Args:
            id_ (int): Database ID for delay profile

        Returns:
            Response: HTTP Response
        """

        return self._delete(f"delayprofile/{id_}", self.ver_uri)

    # GET /manualimport
    def get_manual_import(
        self,
        folder: str,
        download_id: Optional[str] = None,
        author_id: Optional[int] = None,
        filter_existing_files: Optional[bool] = None,
        replace_existing_files: Optional[bool] = None,
    ) -> JsonArray:
        """Gets a manual import list

        Args:
            downloadId (str): Download IDs
            author_id (int, optional): Author Database ID. Defaults to None.
            folder (Optional[str], optional): folder name. Defaults to None.
            filterExistingFiles (bool, optional): filter files. Defaults to True.
            replaceExistingFiles (bool, optional): replace files. Defaults to True.

        Returns:
            JsonArray: List of dictionaries with items
        """
        params: dict[str, Union[str, int, bool]] = {"folder": folder}
        if download_id:
            params["downloadId"] = download_id
        if author_id:
            params["authorId"] = author_id
        if filter_existing_files:
            params["filterExistingFiles"] = filter_existing_files
        if replace_existing_files:
            params["replaceExistingFiles"] = replace_existing_files

        return self._get("manualimport", self.ver_uri, params=params)

    # PUT /manualimport
    def upd_manual_import(self, data: JsonObject) -> JsonObject:
        """Update a manual import

        Note:
            To be used in conjunction with get_manual_import()

        Args:
            data (JsonObject): Data containing changes

        Returns:
            JsonObject: Dictionary of updated record
        """
        return self._put("manualimport", self.ver_uri, data=data)

    # GET /edition
    def get_edition(self, id_: int) -> JsonArray:
        """Get edition's for specific book

        Args:
            id_ (int): Database ID of book

        Returns:
            JsonObject: Dictionary of editions
        """

        return self._get("edition", self.ver_uri, params={"bookId": id_})
