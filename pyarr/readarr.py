from typing import Any, Optional, Union

from requests import Response

from pyarr.types import JsonDataType

from .base import BaseArrAPI
from .exceptions import PyarrMissingArgument, PyarrMissingProfile
from .models.common import PyarrSortDirection
from .models.readarr import (
    ReadarrAuthorMonitor,
    ReadarrBookTypes,
    ReadarrCommands,
    ReadarrSortKeys,
)


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

    def lookup(self, term: str) -> list[dict[str, JsonDataType]]:
        """Search for an author / book

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
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        return self._get("search", self.ver_uri, params={"term": term})

    # GET /book/lookup
    def lookup_book(self, term: str) -> list[dict[str, JsonDataType]]:
        """Searches for new books using a term, goodreads ID, isbn or asin.

        Args:
            term (str): Search term::

                goodreads:656
                isbn:067003469X
                asin:B00JCDK5ME

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        return self._get("book/lookup", self.ver_uri, {"term": term})

    # GET /author/lookup/
    def lookup_author(self, term: str) -> list[dict[str, JsonDataType]]:
        """Searches for new authors using a term

        Args:
            term (str): Author name or book

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        params = {"term": term}
        return self._get("author/lookup", self.ver_uri, params)

    def _book_json(
        self,
        id_: str,
        book_id_type: ReadarrBookTypes,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        search_for_new_book: bool = False,
        author_monitor: ReadarrAuthorMonitor = ReadarrAuthorMonitor.ALL,
        author_search_for_missing_books: bool = False,
    ) -> dict[str, JsonDataType]:
        """Constructs the JSON required to add a new book to Readarr

        Args:
            id_ (str): Book ID from Goodreads, ISBN or ASIN
            book_id_type (ReadarrBookTypes): Type of book ID
            root_dir (str): Root directory for books
            quality_profile_id (Optional[int], optional): Quality profile ID. Defaults to None.
            metadata_profile_id (Optional[int], optional): Metadata profile ID. Defaults to None.
            monitored (bool, optional): Monitor for book. Defaults to True.
            search_for_new_book (bool, optional): Search for new book on adding. Defaults to False.
            author_monitor (ReadarrAuthorMonitor, optional): Monitor the author. Defaults to ReadarrAuthorMonitor.ALL.
            author_search_for_missing_books (bool, optional): Search for other missing books by author. Defaults to False.

        Raises:
            PyarrMissingProfile: Error if Metadata or Quality profile ID are incorrect

        Returns:
            dict[str, JsonDataType]: Dictionary of generated record
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
                metadata_profile: Union[
                    list[dict[str, Any]], dict[str, Any]
                ] = self.get_metadata_profile()
                if isinstance(metadata_profile, list):
                    metadata_profile_id = metadata_profile[0]["id"]
            except IndexError as exception:
                raise PyarrMissingProfile(
                    "There is no Metadata Profile setup"
                ) from exception
        book: dict[str, Any] = self.lookup_book(f"{book_id_type}:{id_}")[0]
        book["author"] = {}
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

        return book

    def _author_json(
        self,
        term: str,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        author_monitor: ReadarrAuthorMonitor = ReadarrAuthorMonitor.NONE,
        search_for_missing_books: bool = False,
    ) -> dict[str, JsonDataType]:
        """Constructs the JSON required to add a new book to Readarr

        Args:
            term (str): Search term
            root_dir (str): Root directory for books
            quality_profile_id (Optional[int], optional): Quality profile ID. Defaults to None.
            metadata_profile_id (Optional[int], optional): Metadata profile ID. Defaults to None.
            monitored (bool, optional): Monitor this author. Defaults to True.
            author_monitor (ReadarrAuthorMonitor, optional): Monitor the author. Defaults to ReadarrAuthorMonitor.NONE.
            search_for_missing_books (bool, optional): Search for missing books by the author. Defaults to False.

        Raises:
            PyarrMissingProfile: Error if Metadata or Quality profile ID are incorrect

        Returns:
            dict[str, JsonDataType]: Dictionary of author data
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
                metadata_profile: Union[
                    list[dict[str, Any]], dict[str, Any]
                ] = self.get_metadata_profile()
                if isinstance(metadata_profile, list):
                    metadata_profile_id = metadata_profile[0]["id"]
            except IndexError as exception:
                raise PyarrMissingProfile(
                    "There is no Metadata Profile setup"
                ) from exception

        author: dict[str, Any] = self.lookup_author(term)[0]

        author["metadataProfileId"] = metadata_profile_id
        author["qualityProfileId"] = quality_profile_id
        author["rootFolderPath"] = root_dir
        author["addOptions"] = {
            "monitor": author_monitor,
            "searchForMissingBooks": search_for_missing_books,
        }
        author["monitored"] = monitored

        return author

    # COMMAND

    # GET /command/:id
    def get_command(
        self, id_: Optional[int] = None
    ) -> Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]:
        """Queries the status of a previously started command, or all currently started commands.

        Args:
            id_ (Optional[int], optional): Database ID of the command. Defaults to None.

        Returns:
            Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]: List of dictionaries with items
        """
        path = f"command/{id_}" if id_ else "command"
        return self._get(path, self.ver_uri)

    # POST /command
    def post_command(
        self,
        name: ReadarrCommands,
        **kwargs: Optional[dict[str, Union[int, list[int]]]],
    ) -> dict[str, JsonDataType]:
        """Performs any of the predetermined Readarr command routines

        Args:
            name (ReadarrCommands): Command name that should be executed
            **kwargs: Additional parameters for specific commands

        Note:
            For available commands and required `**kwargs` see the `ReadarrCommands` model


        Returns:
            dict[str, JsonDataType]: Dictionary of command run
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
    ) -> dict[str, JsonDataType]:
        """Gets missing episode (episodes without files)

        Args:
            page (int, optional): Page number to return. Defaults to None.
            page_size (int, optional): Number of items per page. Defaults to None.
            sort_key (ReadarrSortKeys, optional): id, title, ratings, bookid, or quality. (Others do not apply). Defaults to None.
            sort_dir (PyarrSortDirection, optional): Direction to sort the items. Defaults to None,

        Returns:
            dict[str, JsonDataType]: List of dictionaries with items
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
    ) -> dict[str, JsonDataType]:
        """Get wanted items where the cutoff is unmet

        Args:
            page (int, optional): Page number to return. Defaults to None.
            page_size (int, optional):  Number of items per page. Defaults to None.
            sort_key (ReadarrSortKeys, optional): id, title, ratings, bookid, or quality". (others do not apply). Defaults to None.
            sort_dir (PyarrSortDirection, optional): Direction to sort. Defaults to None.
            monitored (bool, optional): Search for monitored only. Defaults to None.

        Returns:
            dict[str, JsonDataType]: List of dictionaries with items
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
    ) -> dict[str, JsonDataType]:
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
            dict[str, JsonDataType]: List of dictionaries with items
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

    # GET /metadataprofile/{id}
    def get_metadata_profile(
        self, id_: Optional[int] = None
    ) -> Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]:
        """Gets all metadata profiles or specific one with ID

        Args:
            id_ (Optional[int], optional): Metadata profile id from database. Defaults to None.

        Returns:
            Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]: List of dictionaries with items
        """
        path = f"metadataprofile/{id_}" if id_ else "metadataprofile"
        return self._get(path, self.ver_uri)

    # GET /delayprofile/{id}
    def get_delay_profile(
        self, id_: Optional[int] = None
    ) -> Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]:
        """Gets all delay profiles or specific one with ID

        Args:
            id_ (Optional[int], optional): Metadata profile ID from database. Defaults to None.

        Returns:
            Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]: List of dictionaries with items
        """
        path = f"delayprofile/{id_}" if id_ else "delayprofile"
        return self._get(path, self.ver_uri)

    # GET /releaseprofile/{id}
    def get_release_profile(
        self, id_: Optional[int] = None
    ) -> Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]:
        """Gets all release profiles or specific one with ID

        Args:
            id_ (Optional[int], optional): Release profile ID from database. Defaults to None.

        Returns:
            Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]: List of dictionaries with items
        """
        path = f"releaseprofile/{id_}" if id_ else "releaseprofile"
        return self._get(path, self.ver_uri)

    ## BOOKS

    # GET /book and /book/{id}
    def get_book(
        self, id_: Optional[int] = None
    ) -> Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]:
        """Returns all books in your collection or the book with the matching
        book ID if one is found.

        Args:
            id_ (Optional[int], optional): Database id for book. Defaults to None.

        Returns:
            Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]: List of dictionaries with items
        """
        path = f"book/{id_}" if id_ else "book"
        return self._get(path, self.ver_uri)

    # POST /book
    def add_book(
        self,
        id_: str,
        book_id_type: ReadarrBookTypes,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        search_for_new_book: bool = False,
        author_monitor: ReadarrAuthorMonitor = ReadarrAuthorMonitor.ALL,
        author_search_for_missing_books: bool = False,
    ) -> dict[str, JsonDataType]:
        """Adds a new book and  its associated author (if not already added)

        Args:
            id_ (str): goodreads, isbn, asin ID for the book
            book_id_type (str): goodreads / isbn / asin
            root_dir (str): Directory for book to be stored
            quality_profile_id (int, optional): quality profile id. Defaults to 1.
            metadata_profile_id (int, optional): metadata profile id. Defaults to 0.
            monitored (bool, optional): should the book be monitored. Defaults to True.
            search_for_new_book (bool, optional): search for the book to download now. Defaults to False.
            author_monitor (str, optional): monitor the author for new books. Defaults to "all".
            author_search_for_missing_books (bool, optional): search for missing books from this author. Defaults to False.

        Returns:
            dict[str, JsonDataType]: Dictionary of added record
        """

        book_json: dict[str, Any] = self._book_json(
            id_,
            book_id_type,
            root_dir,
            quality_profile_id,
            metadata_profile_id,
            monitored,
            search_for_new_book,
            author_monitor,
            author_search_for_missing_books,
        )
        return self._post("book", self.ver_uri, data=book_json)

    # PUT /book/{id}
    def upd_book(
        self, id_: int, data: dict[str, JsonDataType]
    ) -> dict[str, JsonDataType]:
        """Update the given book, currently only monitored is changed, all other modifications are ignored.

        Note:
            To be used in conjunction with get_book()

        Args:
            id_ (int): Book database ID to update
            data (dict[str, JsonDataType]): All parameters to update book

        Returns:
            dict[str, JsonDataType]: Dictionary with updated record
        """
        return self._put(f"book/{id_}", self.ver_uri, data=data)

    # DELETE /book/{id}
    def del_book(
        self,
        id_: int,
        delete_files: Optional[bool] = None,
        import_list_exclusion: Optional[bool] = None,
    ) -> Union[Response, dict[str, JsonDataType], dict[Any, Any]]:
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

    # AUTHOR

    # GET /author and /author/{id}
    def get_author(
        self, id_: Optional[int] = None
    ) -> Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]:
        """Returns all authors in your collection or the author with the matching ID if one is found.

        Args:
            id_ (Optional[int], optional): Database ID for author. Defaults to None.

        Returns:
            Union[list[dict[str, JsonDataType]], dict[str, JsonDataType]]: List of dictionaries with items
        """
        path = f"author/{id_}" if id_ else "author"
        return self._get(path, self.ver_uri)

    # POST /author/
    def add_author(
        self,
        term: str,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        author_monitor: ReadarrAuthorMonitor = ReadarrAuthorMonitor.NONE,
        author_search_for_missing_books: bool = False,
    ) -> dict[str, JsonDataType]:
        """Adds an authorbased on search term, must be author name or book by goodreads / isbn / asin ID

        Args:
            term (str): Author name or Author book by ID
            root_dir (str): Directory for book to be stored
            quality_profile_id (int, optional): Quality profile id. Defaults to 1.
            metadata_profile_id (int, optional): Metadata profile id. Defaults to 0.
            monitored (bool, optional): Should the author be monitored. Defaults to True.
            author_monitor (ReadarrAuthorMonitor, optional): What level  should the author be monitored. Defaults to "ReadarrAuthorMonitor.NONE".
            author_search_for_missing_books (bool, optional): Search for any missing books by the author. Defaults to False.

        Returns:
            dict[str, JsonDataType]: Dictonary of added record
        """
        author_json: dict[str, Any] = self._author_json(
            term,
            root_dir,
            quality_profile_id,
            metadata_profile_id,
            monitored,
            author_monitor,
            author_search_for_missing_books,
        )
        return self._post("author", self.ver_uri, data=author_json)

    # PUT /author/{id}
    def upd_author(
        self, id_: int, data: dict[str, JsonDataType]
    ) -> dict[str, JsonDataType]:
        """Update the given author, currently only monitored is changed, all other modifications are ignored.

        Note:
            To be used in conjunction with get_author()

        Args:
            id_ (int): Author database ID to update
            data (dict[str, JsonDataType]): All parameters to update author

        Returns:
            dict[str, JsonDataType]: Dictionary with updated record
        """
        return self._put(f"author/{id_}", self.ver_uri, data=data)

    # DELETE /author/{id}
    def del_author(
        self,
        id_: int,
        delete_files: Optional[bool] = None,
        import_list_exclusion: Optional[bool] = None,
    ) -> Union[Response, dict[str, JsonDataType], dict[Any, Any]]:
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
    def get_log_file(self) -> list[dict[str, JsonDataType]]:
        """Get log file

        Returns:
            list[dict[str, JsonDataType]]: List of dictionaries with items
        """
        return self._get("log/file", self.ver_uri)

    # CONFIG

    # POST /rootFolder/
    def add_root_folder(
        self,
        name: str,
        path: str,
        is_calibre_lib: bool = False,
        calibre_host: str = "localhost",
        calibre_port: int = 8080,
        use_ssl: bool = False,
        output_profile: str = "default",
        default_tags: Optional[list] = None,
        default_quality_profile_id: int = 1,
        default_metadata_profile_id: int = 1,
    ) -> dict[str, JsonDataType]:
        """Add a new location to store files

        Args:
            name (str): Friendly Name for folder
            path (str): Location the files should be stored
            is_calibre_lib (bool, optional): Use Calibre Content Server. Defaults to False.
            calibre_host (str, optional): Calibre Content Server address. Defaults to "localhost".
            calibre_port (int, optional): Calibre Content Server port. Defaults to 8080.
            use_ssl (bool, optional): Calibre Content Server SSL. Defaults to False.
            output_profile (str, optional): Books to monitor. Defaults to "default".
            default_tags (Optional[list], optional): List of tags to apply. Defaults to None.
            default_quality_profile_id (int, optional): Quality Profile. Defaults to 1.
            default_metadata_profile_id (int, optional): Metadata Profile. Defaults to 1.

        Returns:
            dict[str, JsonDataType]: Dictionary of added record
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
    def get_metadata_provider(self) -> dict[str, JsonDataType]:
        """Get metadata provider from settings/metadata

        Returns:
            dict[str, JsonDataType]: Dictionary of record
        """
        return self._get("config/metadataProvider", self.ver_uri)

    # PUT /config/metadataProvider
    def upd_metadata_provider(
        self, data: dict[str, JsonDataType]
    ) -> dict[str, JsonDataType]:
        """Update the metadata provider data.

        Note:
            To be used in conjunction with get_metadata_provider()

        Args:
            data (dict[str, JsonDataType]): All parameters to update

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        return self._put("config/metadataProvider", self.ver_uri, data=data)
