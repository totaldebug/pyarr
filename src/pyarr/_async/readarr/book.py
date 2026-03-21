from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray, JsonObject


class Book(CommonActions):
    """Book actions for Readarr."""

    async def get(self, item_id: int | None = None) -> JsonArray | JsonObject:
        """Returns books by ID or all books.

        Args:
            item_id (int | None, optional): Database ID for book. Defaults to None.

        Returns:
            JsonArray | JsonObject: List of dictionaries with items or a single dictionary.
        """
        return await self._get("book", item_id=item_id)

    async def add(
        self,
        book: JsonObject,
        root_dir: str,
        quality_profile_id: int,
        metadata_profile_id: int,
        monitored: bool = True,
        search_for_new_book: bool = False,
        author_monitor: str = "all",
        author_search_for_missing_books: bool = False,
    ) -> JsonObject:
        """Add a new book and its associated author.

        Args:
            book (JsonObject): A book object from `lookup()`.
            root_dir (str): The root directory for the books to be saved.
            quality_profile_id (int): Quality profile ID.
            metadata_profile_id (int): Metadata profile ID.
            monitored (bool, optional): Monitor the book. Defaults to True.
            search_for_new_book (bool, optional): Look for new books. Defaults to False.
            author_monitor (str, optional): Author monitor type. Defaults to "all".
            author_search_for_missing_books (bool, optional): Search missing books. Defaults to False.

        Returns:
            JsonObject: A copy of the added book.
        """
        book["author"]["rootFolderPath"] = root_dir
        book["author"]["metadataProfileId"] = metadata_profile_id
        book["author"]["qualityProfileId"] = quality_profile_id
        book["author"]["addOptions"] = {
            "monitor": author_monitor,
            "searchForMissingBooks": author_search_for_missing_books,
        }
        book["monitored"] = monitored
        book["author"]["manualAdd"] = True
        book["addOptions"] = {"searchForNewBook": search_for_new_book}

        response = await self.handler.request("book", method="POST", json_data=book)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'book' endpoint")

    async def update(self, book: JsonObject, editions: JsonArray) -> JsonObject:
        """Update the given book.

        Args:
            book (JsonObject): All parameters to update book.
            editions (JsonArray): List of editions to update.

        Returns:
            JsonObject: Dictionary with updated record.
        """
        book["editions"] = editions
        response = await self.handler.request("book", method="PUT", json_data=book)
        if isinstance(response, dict):
            return response
        raise ValueError("Expected a dictionary response from the 'book' endpoint")

    async def monitor(self, book_ids: list[int], monitored: bool = True) -> JsonArray:
        """Update book monitored status.

        Args:
            book_ids (list[int]): All book IDs to be updated.
            monitored (bool, optional): True or False. Defaults to True.

        Returns:
            JsonArray: list of dictionaries containing updated records.
        """
        json_data = {"bookIds": book_ids, "monitored": monitored}
        response = await self.handler.request("book/monitor", method="PUT", json_data=json_data)
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'book/monitor' endpoint")

    async def delete(
        self,
        item_id: int,
        delete_files: bool = False,
        import_list_exclusion: bool = False,
    ) -> None:
        """Delete the book with the given ID.

        Args:
            item_id (int): Database ID for book.
            delete_files (bool, optional): Delete folder and files. Defaults to False.
            import_list_exclusion (bool, optional): Add exclusion. Defaults to False.
        """
        params: dict[str, bool] = {
            "deleteFiles": delete_files,
            "addImportListExclusion": import_list_exclusion,
        }
        await self.handler.request(f"book/{item_id}", method="DELETE", params=params)

    async def lookup(self, term: str) -> JsonArray:
        """Search for a book to add to the database.

        Args:
            term (str): Search term.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("book/lookup", params={"term": term})
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'book/lookup' endpoint")
