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

    # CALENDAR
    # Moved to base api

    ## COMMAND

    # GET /command
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
    ):
        pass

        # path = "book"
        # res = self.request_post(path, data=book_json)
        # return res

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
        params = {"term": term}
        path = "book/lookup"
        return self.request_get(path, self.ver_uri, params=params)

    ## LOG

    # GET /log/file
    def get_log_file(self):
        """Get log file

        Returns:
            JSON: Array
        """
        path = "log/file"
        return self.request_get(path, self.ver_uri)
