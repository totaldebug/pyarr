from typing import Any, Optional, Union

from requests import Response

from .base import BaseArrAPI
from .const import PAGE, PAGE_SIZE
from .exceptions import PyarrMissingProfile
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

    def _book_json(
        self,
        db_id: str,
        book_id_type: ReadarrBookTypes,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        search_for_new_book: bool = False,
        author_monitor: ReadarrAuthorMonitor = ReadarrAuthorMonitor.ALL,
        author_search_for_missing_books: bool = False,
    ) -> dict[str, Any]:
        """Constructs the JSON required to add a new book to Readarr

        Args:
            db_id (str): Book ID from Goodreads, ISBN or ASIN
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
            dict[str, Any]: Dictionary of generated record
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
        book = self.lookup_book(f"{book_id_type}:{db_id}")[0]

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
    ) -> dict[str, Any]:
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
            dict[str, Any]: Dictionary of author data
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

        author = self.lookup_author(term)[0]

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
    def get_command(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Queries the status of a previously started command, or all currently started commands.

        Args:
            id_ (Optional[int], optional): Database ID of the command. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"command/{id_}" if id_ else "command"
        return self.assert_return(path, self.ver_uri, list)

    # POST /command
    # TODO: confirm return type & Kwargs
    def post_command(self, name: ReadarrCommands, **kwargs) -> Any:
        """Performs any of the predetermined Readarr command routines

        Args:
            name (ReadarrCommands): Command name that should be executed
            **kwargs: Additional parameters for specific commands

        Returns:
            _type_: _description_
        """
        data = {
            "name": name,
            **kwargs,
        }
        return self._post("command", self.ver_uri, data=data)

    ## WANTED (MISSING)

    # GET /wanted/missing
    def get_missing(
        self,
        sort_key: ReadarrSortKeys = ReadarrSortKeys.BOOK_ID,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_dir: PyarrSortDirection = PyarrSortDirection.ASC,
    ) -> dict[str, Any]:
        """Gets missing episode (episodes without files)

        Args:
            sort_key (ReadarrSortKeys, optional): id, title, ratings, bookid, or quality. (Others do not apply). Defaults to ReadarrSortKeys.BOOK_ID.
            page (int, optional): Page number to return. Defaults to PAGE.
            page_size (int, optional): Number of items per page. Defaults to PAGE_SIZE.
            sort_dir (PyarrSortDirection, optional): Direction to sort the items. Defaults to PyarrSortDirection.ASC.

        Returns:
            dict[str, Any]: List of dictionaries with items
        """
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDir": sort_dir,
        }
        return self.assert_return("wanted/missing", self.ver_uri, dict, params)

    # GET /wanted/cutoff
    def get_cutoff(
        self,
        sort_key: ReadarrSortKeys = ReadarrSortKeys.BOOK_ID,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_dir: PyarrSortDirection = PyarrSortDirection.DESC,
        monitored: bool = True,
    ) -> dict[str, Any]:
        """Get wanted items where the cutoff is unmet

        Args:
            sort_key (ReadarrSortKeys, optional): id, title, ratings, bookid, or quality". (others do not apply). Defaults to ReadarrSortKeys.BOOK_ID.
            page (int, optional): Page number to return. Defaults to PAGE.
            page_size (int, optional):  Number of items per page. Defaults to PAGE_SIZE.
            sort_dir (PyarrSortDirection, optional): Direction to sort. Defaults to PyarrSortDirection.DESC.
            monitored (bool, optional): Search for monitored only. Defaults to True.

        Returns:
            dict[str, Any]: List of dictionaries with items
        """
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDir": sort_dir,
            "monitored": monitored,
        }
        return self.assert_return("wanted/cutoff", self.ver_uri, dict, params)

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page: int = PAGE,
        page_size: int = PAGE_SIZE,
        sort_dir: PyarrSortDirection = PyarrSortDirection.ASC,
        sort_key: ReadarrSortKeys = ReadarrSortKeys.TIMELEFT,
        unknown_authors: bool = False,
        include_author: bool = False,
        include_book: bool = False,
    ) -> dict[str, Any]:
        """Get current download information

        Args:
            page (int, optional): Page number. Defaults to PAGE.
            page_size (int, optional): Number of items per page. Defaults to PAGE_SIZE.
            sort_dir (PyarrSortDirection, optional): Direction to sort. Defaults to PyarrSortDirection.ASC.
            sort_key (ReadarrSortKeys, optional): Field to sort by. Defaults to ReadarrSortKeys.TIMELEFT.
            unknown_authors (bool, optional): Include items with an unknown author. Defaults to False.
            include_author (bool, optional): Include the author. Defaults to False.
            include_book (bool, optional): Include the book. Defaults to False.

        Returns:
            dict[str, Any]: List of dictionaries with items
        """
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDirection": sort_dir,
            "includeUnknownAuthorItems": unknown_authors,
            "includeAuthor": include_author,
            "includeBook": include_book,
        }
        return self.assert_return("queue", self.ver_uri, dict, params)

    # GET /metadataprofile/{id}
    def get_metadata_profile(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Gets all metadata profiles or specific one with ID

        Args:
            id_ (Optional[int], optional): Metadata profile id from database. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"metadataprofile/{id_}" if id_ else "metadataprofile"
        return self.assert_return(path, self.ver_uri, list)

    # GET /delayprofile/{id}
    def get_delay_profile(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Gets all delay profiles or specific one with ID

        Args:
            id_ (Optional[int], optional): Metadata profile ID from database. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"delayprofile/{id_}" if id_ else "delayprofile"
        return self.assert_return(path, self.ver_uri, list)

    # GET /releaseprofile/{id}
    def get_release_profile(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Gets all release profiles or specific one with ID

        Args:
            id_ (Optional[int], optional): Release profile ID from database. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"releaseprofile/{id_}" if id_ else "releaseprofile"
        return self.assert_return(path, self.ver_uri, list)

    ## BOOKS

    # GET /book and /book/{id}
    def get_book(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Returns all books in your collection or the book with the matching
        book ID if one is found.

        Args:
            id_ (Optional[int], optional): Database id for book. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"book/{id_}" if id_ else "book"
        return self.assert_return(path, self.ver_uri, list)

    # GET /book/lookup
    def lookup_book(self, term: str) -> list[dict[str, Any]]:
        """Searches for new books using a term, goodreads ID, isbn or asin.

        Args:
            term (str): Search term::

                goodreads:656
                isbn:067003469X
                asin:B00JCDK5ME

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("book/lookup", self.ver_uri, list, {"term": term})

    # POST /book
    def add_book(
        self,
        db_id: str,
        book_id_type: ReadarrBookTypes,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        search_for_new_book: bool = False,
        author_monitor: ReadarrAuthorMonitor = ReadarrAuthorMonitor.ALL,
        author_search_for_missing_books: bool = False,
    ) -> dict[str, Any]:
        """Adds a new book and  its associated author (if not already added)

        Args:
            db_id (int): goodreads, isbn, asin ID for the book
            book_id_type (str): goodreads / isbn / asin
            root_dir (str): Directory for book to be stored
            quality_profile_id (int, optional): quality profile id. Defaults to 1.
            metadata_profile_id (int, optional): metadata profile id. Defaults to 0.
            monitored (bool, optional): should the book be monitored. Defaults to True.
            search_for_new_book (bool, optional): search for the book to download now. Defaults to False.
            author_monitor (str, optional): monitor the author for new books. Defaults to "all".
            author_search_for_missing_books (bool, optional): search for missing books from this author. Defaults to False.

        Returns:
            dict[str, Any]: Dictionary of added record
        """

        book_json = self._book_json(
            db_id,
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
    def upd_book(self, id_: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update the given book, currently only monitored is changed, all other modifications are ignored.

        Note:
            To be used in conjunction with get_book()

        Args:
            id_ (int): Book database ID to update
            data (dict[str, Any]): All parameters to update book

        Returns:
            dict[str, Any]: Dictionary with updated record
        """
        return self._put(f"book/{id_}", self.ver_uri, data=data)

    # DELETE /book/{id}
    def del_book(
        self, id_: int, delete_files: bool = False, import_list_exclusion: bool = True
    ) -> Response:
        """Delete the book with the given ID

        Args:
            id_ (int): Database ID for book
            delete_files (bool, optional): If true book folder and files will be deleted. Defaults to False.
            import_list_exclusion (bool, optional): Add an exclusion so book doesn't get re-added. Defaults to True.

        Returns:
            Response: HTTP Response
        """
        params = {
            "deleteFiles": delete_files,
            "addImportListExclusion": import_list_exclusion,
        }
        return self._delete(f"book/{id_}", self.ver_uri, params=params)

    # AUTHOR

    # GET /author and /author/{id}
    def get_author(self, id_: Optional[int] = None) -> list[dict[str, Any]]:
        """Returns all authors in your collection or the author with the matching ID if one is found.

        Args:
            id_ (Optional[int], optional): Database ID for author. Defaults to None.

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        path = f"author/{id_}" if id_ else "author"
        return self.assert_return(path, self.ver_uri, list)

    # GET /author/lookup/
    def lookup_author(self, term: str) -> list[dict[str, Any]]:
        """Searches for new authors using a term

        Args:
            term (str): Author name or book

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        params = {"term": term}
        return self.assert_return("author/lookup", self.ver_uri, list, params)

    # POST /author/
    def add_author(
        self,
        search_term: str,
        root_dir: str,
        quality_profile_id: Optional[int] = None,
        metadata_profile_id: Optional[int] = None,
        monitored: bool = True,
        author_monitor: ReadarrAuthorMonitor = ReadarrAuthorMonitor.NONE,
        author_search_for_missing_books: bool = False,
    ) -> dict[str, Any]:
        """Adds an authorbased on search term, must be author name or book by goodreads / isbn / asin ID

        Args:
            search_term (str): Author name or Author book by ID
            root_dir (str): Directory for book to be stored
            quality_profile_id (int, optional): Quality profile id. Defaults to 1.
            metadata_profile_id (int, optional): Metadata profile id. Defaults to 0.
            monitored (bool, optional): Should the author be monitored. Defaults to True.
            author_monitor (ReadarrAuthorMonitor, optional): What level  should the author be monitored. Defaults to "ReadarrAuthorMonitor.NONE".
            author_search_for_missing_books (bool, optional): Search for any missing books by the author. Defaults to False.

        Returns:
            dict[str, Any]: Dictonary of added record
        """
        author_json = self._author_json(
            search_term,
            root_dir,
            quality_profile_id,
            metadata_profile_id,
            monitored,
            author_monitor,
            author_search_for_missing_books,
        )
        return self._post("author", self.ver_uri, data=author_json)

    # PUT /author/{id}
    def upd_author(self, id_: int, data: dict[str, Any]) -> dict[str, Any]:
        """Update the given author, currently only monitored is changed, all other modifications are ignored.

        Note:
            To be used in conjunction with get_author()

        Args:
            id_ (int): Author database ID to update
            data (dict[str, Any]): All parameters to update author

        Returns:
            dict[str, Any]: Dictionary with updated record
        """
        return self._put(f"author/{id_}", self.ver_uri, data=data)

    # DELETE /author/{id}
    def del_author(
        self, id_: int, delete_files: bool = False, import_list_exclusion: bool = True
    ) -> Response:
        """Delete the author with the given ID

        Args:
            id_ (int): Database ID for author
            delete_files (bool, optional): If true author folder and files will be deleted. Defaults to False.
            import_list_exclusion (bool, optional): Add an exclusion so author doesn't get re-added. Defaults to True.

        Returns:
            Response: HTTP Response
        """
        params = {
            "deleteFiles": delete_files,
            "addImportListExclusion": import_list_exclusion,
        }
        return self._delete(f"author/{id_}", self.ver_uri, params=params)

    ## LOG

    # GET /log/file
    def get_log_file(self) -> list[dict[str, Any]]:
        """Get log file

        Returns:
            list[dict[str, Any]]: List of dictionaries with items
        """
        return self.assert_return("log/file", self.ver_uri, list)

    # CONFIG

    # POST /rootFolder/
    def add_root_folder(
        self,
        name: str,
        directory: str,
        is_calibre_lib: bool = False,
        calibre_host: str = "localhost",
        calibre_port: int = 8080,
        use_ssl: bool = False,
        output_profile: str = "default",
        default_tags: Union[list, None] = None,
        default_quality_profile_id: int = 1,
        default_metadata_profile_id: int = 1,
    ) -> dict[str, Any]:
        """Add a new root directory to the Readarr Server

        Args:
            name (str): Friendly Name for folder
            directory (str): Directory to use e.g. /books/
            is_calibre_lib (bool, optional): Use Calibre Content Server. Defaults to False.
            calibre_host (str, optional): Calibre Content Server address. Defaults to "localhost".
            calibre_port (int, optional): Calibre Content Server port. Defaults to 8080.
            use_ssl (bool, optional): Calibre Content Server SSL. Defaults to False.
            output_profile (str, optional): Books to monitor. Defaults to "default".
            default_tags (Union[list, None], optional): List of tags to apply. Defaults to None.
            default_quality_profile_id (int, optional): Quality Profile. Defaults to 1.
            default_metadata_profile_id (int, optional): Metadata Profile. Defaults to 1.

        Returns:
            dict[str, Any]: Dictionary of added record
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
            "path": directory,
        }
        return self._post("rootFolder", self.ver_uri, data=folder_json)

    # GET /config/metadataProvider
    def get_metadata_provider(self) -> dict[str, Any]:
        """Get metadata provider from settings/metadata

        Returns:
            dict[str, Any]: Dictionary of record
        """
        return self.assert_return("config/metadataProvider", self.ver_uri, dict)

    # PUT /config/metadataProvider
    def upd_metadata_provider(self, data: dict[str, Any]) -> dict[str, Any]:
        """Update the metadata provider data.

        Note:
            To be used in conjunction with get_metadata_provider()

        Args:
            data (dict[str, Any]): All parameters to update

        Returns:
            dict[str, Any]: Dictionary of updated record
        """
        return self._put("config/metadataProvider", self.ver_uri, data=data)
