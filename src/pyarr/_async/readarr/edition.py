from pyarr._async.common.base import CommonActions
from pyarr.types import JsonArray


class Edition(CommonActions):
    """Edition actions for Readarr."""

    async def get(self, book_id: int) -> JsonArray:
        """Get editions for a specific book.

        Args:
            book_id (int): Database ID of book.

        Returns:
            JsonArray: List of dictionaries with items.
        """
        response = await self.handler.request("edition", params={"bookId": book_id})
        if isinstance(response, list):
            return response
        raise ValueError("Expected a list response from the 'edition' endpoint")
