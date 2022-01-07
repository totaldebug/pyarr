from .base import BaseAPI


class ReadarrAPI(BaseAPI):
    """API wrapper for Readarr endpoints."""

    def __init__(self, host_url: str, api_key: str):
        """Initialise Readarr API

        Args:
            host_url (str): URL for Readarr
            api_key (str): API key for Readarr
        """

        ver_uri = "/v1"
        super().__init__(host_url, api_key, ver_uri)

    def _construct_book_json(
        self,
        db_id,
        book_id_type,
        root_dir,
        quality_profile_id=1,
        metadata_profile_id=0,
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

        book = self.lookup_book(book_id_type + ":" + str(db_id))[0]

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

    def _construct_author_json(
        self,
        term,
        root_dir,
        quality_profile_id=1,
        metadata_profile_id=1,
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
    def get_missing(self, sort_key="releaseDate", page=1, page_size=10, sort_dir="asc"):
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

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page=1,
        page_size=10,
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

    # GET /metadataprofile
    def get_metadata_profiles(self):
        """Gets all metadata profiles

        Returns:
            JSON: Array
        """
        path = "metadataprofile"
        return self.request_get(path, self.ver_uri)

    # GET /delayprofile
    def get_delay_profiles(self):
        """Gets all delay profiles

        Returns:
            JSON: Array
        """
        path = "/delayprofile"
        return self.request_get(path, self.ver_uri)

    # GET /releaseprofile
    def get_release_profiles(self):
        """Gets all release profiles

        Returns:
            JSON: Array
        """
        path = "releaseprofile"
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

    # POST /book

    def add_book(
        self,
        db_id,
        book_id_type,
        root_dir,
        quality_profile_id=1,
        metadata_profile_id=0,
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

        book_json = self._construct_book_json(
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

    # PUT /book
    def upd_book(self):
        pass

        # path = "book"
        # res = self.request_put(path, data=data)
        # return res

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
        params = {"term": term}
        path = "book/lookup"
        return self.request_get(path, self.ver_uri, params=params)

    def add_author(
        self,
        search_term,
        root_dir,
        quality_profile_id=1,
        metadata_profile_id=1,
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
        author_json = self._construct_author_json(
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

    def add_root_folder(
        self,
        name: str,
        dir: str,
        isCalibreLib: bool = False,
        calibreHost: str = "localhost",
        calibrePort: int = 8080,
        useSsl: bool = False,
        outputProfile: str = "default",
        defaultTags: list = [],
        defaultQualityProfileId: int = 1,
        defaultMetadataProfileId: int = 1,
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
            "isCalibreLibrary": isCalibreLib,
            "host": calibreHost,
            "port": calibrePort,
            "useSsl": useSsl,
            "outputProfile": outputProfile,
            "defaultTags": defaultTags,
            "defaultQualityProfileId": defaultQualityProfileId,
            "defaultMetadataProfileId": defaultMetadataProfileId,
            "name": name,
            "path": dir,
        }
        path = "rootFolder"
        return self.request_post(path, self.ver_uri, data=folder_json)

    def get_metadata_provider(self):
        """Get metadata provider from settings/metadata

        Returns:
            JSON: Array
        """
        path = "config/metadataProvider"
        return self.request_get(path, self.ver_uri)
