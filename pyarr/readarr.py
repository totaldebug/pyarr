from .base import BaseArrAPI
from .const import PAGE, PAGE_SIZE
from .exceptions import PyarrMissingProfile


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
        db_id,
        book_id_type,
        root_dir,
        quality_profile_id=None,
        metadata_profile_id=None,
        monitored=True,
        search_for_new_book=False,
        author_monitor="all",
        author_search_for_missing_books=False,
    ):
        """Constructs the JSON required to add a new book to Readarr

        Args:
            db_id (int): goodreads, isbn, asin ID
            book_id_type (str): goodreads / isbn / asin
            root_dir (str): root directory for books
            quality_profile_id (int, optional): quality profile id. Defaults to 1.
            metadata_profile_id (int, optional): metadata profile id. Defaults to 0.
            monitored (bool, optional): should the book be monitored. Defaults to True.
            search_for_new_book (bool, optional): shour a search for the new book happen. Defaults to False.
            author_monitor (str, optional): monitor the author. Defaults to "all".
            author_search_for_missing_books (bool, optional): search for other missing books by the author. Defaults to False.

        Raises:
            ValueError: error raised if book_id_type is incorrect

        Returns:
            JSON: Array
        """
        book_id_types = ["goodreads", "isbn", "asin"]
        if book_id_type not in book_id_types:
            raise ValueError(f"Invalid book id type. Expected one of: {book_id_types}")
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
        book = self.lookup_book(f"{book_id_type}:{str(db_id)}")[0]

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
        term,
        root_dir,
        quality_profile_id=None,
        metadata_profile_id=None,
        monitored=True,
        author_monitor="none",
        search_for_missing_books=False,
    ):
        """Constructs the JSON required to add a new book to Readarr

        Args:
            search_term (str)
            root_dir (str): root directory for books
            quality_profile_id (int, optional): quality profile id. Defaults to 1.
            metadata_profile_id (int, optional): metadata profile id. Defaults to 0.
            monitored (bool, optional): should the book be monitored. Defaults to True.
            author_monitor (str, optional): monitor the author. Defaults to "none".
            search_for_missing_books (bool, optional): search for other missing books by the author. Defaults to False.

        Returns:
            JSON: Array
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
    def get_command(self, id_=None):
        """Queries the status of a previously started command, or all currently started commands.

        Args:
            id_ (int, optional): Database id of the command. Defaults to None.

        Returns:
            JSON: Array
        """
        path = f"command/{id_}" if id_ else "command"
        return self.request_get(path, self.ver_uri)

    # POST /command
    def post_command(self, name, **kwargs):
        """Performs any of the predetermined Sonarr command routines

        Note:
            For command names and additional kwargs:
                TODO

        Args:
            name (str): command name that should be execured
            **kwargs: additional parameters for specific commands

        Returns:
            JSON: Array
        """
        path = "command"
        data = {
            "name": name,
            **kwargs,
        }
        return self.request_post(path, self.ver_uri, data=data)

    ## WANTED (MISSING)

    # GET /wanted/missing
    def get_missing(
        self, sort_key="releaseDate", page=PAGE, page_size=PAGE_SIZE, sort_dir="asc"
    ):
        """Gets missing episode (episodes without files)

        Args:
            sort_key (str, optional): Books.Id or releaseDate. Defaults to "releaseDate".
            page (int, optional): Page number to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_dir (str, optional): Direction to sort the items. Defaults to "asc".

        Returns:
            JSON: Array
        """
        path = "wanted/missing"
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDir": sort_dir,
        }
        return self.request_get(path, self.ver_uri, params=params)

    # GET /wanted/cutoff
    def get_cutoff(
        self,
        sort_key="releaseDate",
        page=PAGE,
        page_size=PAGE_SIZE,
        sort_dir="descending",
        monitored=True,
    ):
        """Get wanted items where the cutoff is unmet

        Args:
            sort_key (str, optional): field to sort by. Defaults to "releaseDate".
            page (int, optional): page number. Defaults to 1.
            page_size (int, optional): number of results per page_size. Defaults to 10.
            sort_dir (str, optional): direction to sort. Defaults to "descending".
            monitored (bool, optional): search for monitored only. Defaults to True.

        Returns:
            JSON: Array
        """
        path = "wanted/cutoff"
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDir": sort_dir,
            "monitored": monitored,
        }
        return self.request_get(path, self.ver_uri, params=params)

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page=PAGE,
        page_size=PAGE_SIZE,
        sort_dir="ascending",
        sort_key="timeleft",
        unknown_authors=False,
        include_author=False,
        include_book=False,
    ):
        """Get current download information

        Args:
            page (int, optional): page number. Defaults to 1.
            page_size (int, optional): number of results per page_size. Defaults to 10.
            sort_dir (str, optional): direction to sort. Defaults to "ascending".
            sort_key (str, optional): field to sort by. Defaults to "timeleft".
            unknown_authors (bool, optional): Include items with an unknown author. Defaults to False.
            include_author (bool, optional): Include the author. Defaults to False.
            include_book (bool, optional): Include the book. Defaults to False.

        Returns:
            JSON: Array
        """

        path = "queue"
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDirection": sort_dir,
            "includeUnknownAuthorItems": unknown_authors,
            "includeAuthor": include_author,
            "includeBook": include_book,
        }
        return self.request_get(path, self.ver_uri, params=params)

    # GET /metadataprofile/{id}
    def get_metadata_profile(self, id_=None):
        """Gets all metadata profiles or specific one with id_

        Args:
            id_ (int): metadata profile id from database

        Returns:
            JSON: Array
        """
        path = f"metadataprofile/{id_}" if id_ else "metadataprofile"
        return self.request_get(path, self.ver_uri)

    # GET /delayprofile/{id}
    def get_delay_profile(self, id_):
        """Gets all delay profiles or specific one with id_

        Args:
            id_ (int): metadata profile id from database

        Returns:
            JSON: Array
        """
        path = f"delayprofile/{id_}" if id_ else "delayprofile"
        return self.request_get(path, self.ver_uri)

    # GET /releaseprofile/{id}
    def get_release_profile(self, id_=None):
        """Gets all release profiles or specific one with id_

        Args:
            id_ (int): release profile id from database

        Returns:
            JSON: Array
        """
        path = f"releaseprofile/{id_}" if id_ else "releaseprofile"
        return self.request_get(path, self.ver_uri)

    ## BOOKS

    # GET /book and /book/{id}
    def get_book(self, id_=None):
        """Returns all books in your collection or the book with the matching
        book ID if one is found.

        Args:
            id_ (int, optional): Database id for book. Defaults to None.

        Returns:
            JSON: Array
        """
        path = f"book/{id_}" if id_ else "book"
        return self.request_get(path, self.ver_uri)

    # GET /book/lookup
    def lookup_book(self, term):
        """Searches for new books using a term, goodreads ID, isbn or asin.

        Args:
            term (str): search term
            goodreads:656
            isbn:067003469X
            asin:B00JCDK5ME

        Returns:
            JSON: Array
        """
        path = "book/lookup"
        return self.request_get(path, self.ver_uri, params={"term": term})

    # POST /book
    def add_book(
        self,
        db_id,
        book_id_type,
        root_dir,
        quality_profile_id=None,
        metadata_profile_id=None,
        monitored=True,
        search_for_new_book=False,
        author_monitor="all",
        author_search_for_missing_books=False,
    ):
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

        Raises:
            ValueError: error raised if book_id_type is incorrect

        Returns:
            JSON: Array
        """
        book_id_types = ["goodreads", "isbn", "asin"]
        if book_id_type not in book_id_types:
            raise ValueError(f"Invalid book id type. Expected one of: {book_id_types}")

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
        path = "book"
        return self.request_post(path, self.ver_uri, data=book_json)

    # PUT /book/{id}
    def upd_book(self, id_, data):
        """Update the given book, currently only monitored is changed, all other modifications are ignored.

        Note:
            To be used in conjunction with get_book()

        Args:
            id_ (int): Book database ID to update
            data (dict): All parameters to update book

        Returns:
            JSON: Array
        """
        path = f"book/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    # DELETE /book/{id}
    def del_book(self, id_, delete_files=False, import_list_exclusion=True):
        """Delete the book with the given id

        Args:
            id_ (int): Database id for book
            delete_files (bool, optional): If true book folder and files will be deleted. Defaults to False.
            import_list_exclusion (bool, optional): Add an exclusion so book doesn't get re-added. Defaults to True.

        Returns:
            JSON: {}
        """
        params = {
            "deleteFiles": delete_files,
            "addImportListExclusion": import_list_exclusion,
        }
        path = f"book/{id_}"
        return self.request_del(path, self.ver_uri, params=params)

    # AUTHOR

    # GET /author and /author/{id}
    def get_author(self, id_=None):
        """Returns all authors in your collection or the author with the matching ID if one is found.

        Args:
            id_ (int, optional): Database id for author. Defaults to None.

        Returns:
            JSON: Array
        """
        path = f"author/{id_}" if id_ else "author"
        return self.request_get(path, self.ver_uri)

    # GET /author/lookup/
    def lookup_author(self, term):
        """Searches for new authors using a term

        Args:
            term (str): Author name or book

        Returns:
            JSON: Array
        """
        params = {"term": term}
        path = "author/lookup"
        return self.request_get(path, self.ver_uri, params=params)

    # POST /author/
    def add_author(
        self,
        search_term,
        root_dir,
        quality_profile_id=None,
        metadata_profile_id=None,
        monitored=True,
        author_monitor="none",
        author_search_for_missing_books=False,
    ):
        """Adds an authorbased on search term, must be author name or book by goodreads / isbn / asin ID

        Args:
            search_term (str): Author name or Author book by ID
            root_dir (str): Directory for book to be stored
            quality_profile_id (int, optional): Quality profile id. Defaults to 1.
            metadata_profile_id (int, optional): Metadata profile id. Defaults to 0.
            monitored (bool, optional): should the author be monitored. Defaults to True.
            author_monitor (str, optional): What level  should the author be monitored. Defaults to "none".
            author_search_for_missing_books (bool, optional): search for any missing books by the author. Defaults to False.

        Returns:
            JSON: Array
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

        path = "author"
        return self.request_post(path, self.ver_uri, data=author_json)

    # PUT /author/{id}
    def upd_author(self, id_, data):
        """Update the given author, currently only monitored is changed, all other modifications are ignored.

        Note:
            To be used in conjunction with get_author()

        Args:
            id_ (int): Author database ID to update
            data (dict): All parameters to update author

        Returns:
            JSON: Array
        """
        path = f"author/{id_}"
        return self.request_put(path, self.ver_uri, data=data)

    # DELETE /author/{id}
    def del_author(self, id_, delete_files=False, import_list_exclusion=True):
        """Delete the author with the given id

        Args:
            id_ (int): Database id for author
            delete_files (bool, optional): If true author folder and files will be deleted. Defaults to False.
            import_list_exclusion (bool, optional): Add an exclusion so author doesn't get re-added. Defaults to True.

        Returns:
            JSON: Array
        """
        params = {
            "deleteFiles": delete_files,
            "addImportListExclusion": import_list_exclusion,
        }
        path = f"author/{id_}"
        return self.request_del(path, self.ver_uri, params=params)

    ## LOG

    # GET /log/file
    def get_log_file(self):
        """Get log file

        Returns:
            JSON: Array
        """
        path = "log/file"
        return self.request_get(path, self.ver_uri)

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
        default_tags: list = None,
        default_quality_profile_id: int = 1,
        default_metadata_profile_id: int = 1,
    ):
        """Add a new root directory to the Readarr Server

        Args:
            name (str): Friendly Name for folder
            dir (str): Directory to use e.g. /books/
            isCalibreLib (bool, optional): Use Calibre Content Server. Defaults to False.
            calibreHost (str, optional): Calibre Content Server address. Defaults to "localhost".
            calibrePort (int, optional): Calibre Content Server port. Defaults to "8080".
            useSsl (bool, optional): Calibre Content Server SSL. Defaults to False.
            outputProfile (str, optional): Books to monitor. Defaults to "default".
            defaultTags (list, optional): List of tags to apply. Defaults to [].
            defaultQualityProfileId (int, optional): Quality Profile to use. Defaults to 1.
            defaultMetadataProfileId (int, optional): Metadata Profile to use. Defaults to 1.

        Returns:
            JSON: Array
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
        path = "rootFolder"
        return self.request_post(path, self.ver_uri, data=folder_json)

    # GET /config/metadataProvider
    def get_metadata_provider(self):
        """Get metadata provider from settings/metadata

        Returns:
            JSON: Array
        """
        path = "config/metadataProvider"
        return self.request_get(path, self.ver_uri)

    # PUT /config/metadataProvider
    def upd_metadata_provider(self, data):
        """Update the metadata provider data.

        Note:
            To be used in conjunction with get_metadata_provider()

        Args:
            data (dict): All parameters to update

        Returns:
            JSON: Array
        """
        path = "config/metadataProvider"
        return self.request_put(path, self.ver_uri, data=data)
