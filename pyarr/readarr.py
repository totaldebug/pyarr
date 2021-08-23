from .request_api import RequestAPI
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
        if id_:
            path = f"command/{id_}"
        else:
            path = "command"

        res = self.request_get(path, self.ver_uri)
        return res

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
        res = self.request_post(path, self.ver_uri, data=data)
        return res

    ## HISTORY

    # GET /history
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
        res = self.request_get(path, self.ver_uri, params=params)
        return res

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
        path = f"{self.ver_uri}/wanted/missing"
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDir": sort_dir,
        }
        res = self.request_get(path, params=params)
        return res

    ## QUEUE

    # GET /queue
    def get_queue(
        self,
        page=1,
        page_size=10,
        sort_dir="ascending",
        sort_key="timeleft",
        unknown_authors=None,
    ):
        """Get current download information

        Args:
            page (int, optional): Page number to return. Defaults to 1.
            page_size (int, optional): Number of items per page. Defaults to 10.
            sort_dir (str, optional): Direction to sort the items. Defaults to "ascending".
            sort_key (str, optional): series.titke or airDateUtc. Defaults to "timeleft".
            unknown_authors (bool, optional): Include unknown authors in search. Defaults to false.

        Returns:
            JSON: Array
        """

        path = f"{self.ver_uri}/queue"
        params = {
            "sortKey": sort_key,
            "page": page,
            "pageSize": page_size,
            "sortDirection": sort_dir,
            "includeUnknownAuthorItems": unknown_authors,
        }
        res = self.request_get(path, params=params)
        return res

    # DELETE /queue
    def del_queue(self, id_, blacklist=False):
        """Deletes an item from the queue and download client. Optionally blacklist item after deletion.

        Args:
            id_ (int): Database id of queue item
            blacklist (bool, optional): Blacklist item after deletion. Defaults to False.

        Returns:
            JSON: {}
        """
        params = {"id": id_, "blacklist": blacklist}
        path = "queue/"
        res = self.request_del(path, self.ver_uri, params=params)
        return res

    ## PROFILE

    # GET /qualityprofile
    def get_quality_profiles(self):
        """Gets all quality profiles

        Returns:
            JSON: Array
        """
        path = "qualityprofile"
        res = self.request_get(path, self.ver_uri)
        return res

    # GET /metadataprofile
    def get_metadata_profiles(self):
        """Gets all metadata profiles

        Returns:
            JSON: Array
        """
        path = "metadataprofile"
        res = self.request_get(path, self.ver_uri)
        return res

    # GET /delayprofile
    def get_delay_profiles(self):
        """Gets all delay profiles

        Returns:
            JSON: Array
        """
        path = "/delayprofile"
        res = self.request_get(path, self.ver_uri)
        return res

    # GET /releaseprofile
    def get_release_profiles(self):
        """Gets all release profiles

        Returns:
            JSON: Array
        """
        path = "releaseprofile"
        res = self.request_get(path, self.ver_uri)
        return res

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
        if id_:
            path = f"book/{id_}"
        else:
            path = "book"

        res = self.request_get(path, self.ver_uri)
        return res

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
        res = self.request_del(path, self.ver_uri, params=params)
        return res

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
        res = self.request_get(path, self.ver_uri, params=params)
        return res

    # GET /system/task
    def get_task(self, id_=None):
        """Return a list of tasks, or specify a task ID to return single task

        Args:
            id_ (int): ID for task

        Returns:
            JSON: Array
        """
        if id_:
            path = f"system/task/{id_}"
        else:
            path = "system/task"
        res = self.request_get(path, self.ver_uri)
        return res

    ## TAG

    # GET /tag and /tag/{id}
    def get_tag(self, id_=None):
        """Returns all tags or specific tag by database id

        Args:
            id_ (int, optional): Database id for tag. Defaults to None.

        Returns:
            JSON: Array
        """
        if not id_:
            path = "tag"
        else:
            path = f"tag/{id_}"

        res = self.request_get(path, self.ver_uri)
        return res

    # GET /tag and /tag/{id}
    def get_tag_detail(self, id_=None):
        """Returns all tags or specific tag by database id with detailed information

        Args:
            id_ (int, optional): Database id for tag. Defaults to None.

        Returns:
            JSON: Array
        """
        if not id_:
            path = "tag/detail"
        else:
            path = f"tag/detail/{id_}"

        res = self.request_get(path, self.ver_uri)
        return res

    # POST /tag
    def create_tag(self, label):
        """Adds a new tag

        Args:
            label (str): Tag name / label

        Returns:
            JSON: Array
        """
        data = {"label": label}
        path = "tag"
        res = self.request_post(path, self.ver_uri, data=data)
        return res

    # PUT /tag/{id}
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
        res = self.request_put(path, self.ver_uri, data=data)
        return res

    # DELETE /tag/{id}
    def del_tag(self, id_):
        """Delete the tag with the given ID

        Args:
            id_ (int): Database id of tag

        Returns:
            JSON: {}
        """
        path = f"tag/{id_}"
        res = self.request_del(path, self.ver_uri)
        return res

    ## LOG

    # GET /log/file
    def get_log_file(self):
        """Get log file

        Returns:
            JSON: Array
        """
        path = "log/file"
        res = self.request_get(path, self.ver_uri)
        return res
