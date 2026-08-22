from unittest.mock import AsyncMock

import pytest

from pyarr._async.common.base import CommonActions
from pyarr._async.utils.http import RequestHandler


@pytest.mark.parametrize(
    ("path", "item_id", "expected"),
    [
        # Servarr paths carry no trailing slash and must not gain one.
        ("series", 1, "series/1"),
        ("series", None, "series"),
        ("tag/detail", 5, "tag/detail/5"),
        ("system/backup", 3, "system/backup/3"),
        # Dispatcharr's Django routes require the trailing slash on both forms. Appending
        # "/{item_id}" naively produced "channels/channels//1", which Dispatcharr answers
        # with its single page application's HTML at HTTP 200 rather than a 404.
        ("channels/channels/", 1, "channels/channels/1/"),
        ("channels/channels/", None, "channels/channels/"),
        ("plugins/plugins/", "some-key", "plugins/plugins/some-key/"),
        ("core/settings/", 7, "core/settings/7/"),
    ],
)
def test_detail_path_preserves_trailing_slash_convention(path, item_id, expected):
    assert CommonActions._detail_path(path, item_id) == expected


@pytest.mark.parametrize(("path", "item_id", "expected"), [("series", 1, "series/1"), ("core/settings/", 1, "core/settings/1/")])
def test_detail_path_never_doubles_a_slash(path, item_id, expected):
    assert "//" not in CommonActions._detail_path(path, item_id)


@pytest.mark.parametrize(
    ("path", "expected"),
    [("indexer", "indexer/0"), ("channels/channels/", "channels/channels/0/")],
)
def test_item_id_zero_is_an_item_not_an_absence(path, expected):
    """Only None means "no item". Testing truthiness would send a delete for item 0 to
    the collection, which is a very different request."""
    assert CommonActions._detail_path(path, 0) == expected


@pytest.mark.asyncio
async def test_delete_of_item_zero_targets_the_item():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = None
    actions = CommonActions(mock_handler)

    await actions._delete("indexer", item_id=0)

    mock_handler.request.assert_called_with("indexer/0", method="DELETE")


@pytest.mark.asyncio
async def test_get_uses_detail_path():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {}
    actions = CommonActions(mock_handler)

    await actions._get("channels/channels/", item_id=4)
    mock_handler.request.assert_called_with("channels/channels/4/", params=None)

    await actions._get("series", item_id=4)
    mock_handler.request.assert_called_with("series/4", params=None)

    await actions._get("series")
    mock_handler.request.assert_called_with("series", params=None)


@pytest.mark.asyncio
async def test_delete_uses_detail_path():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = None
    actions = CommonActions(mock_handler)

    await actions._delete("channels/channels/", item_id=4)
    mock_handler.request.assert_called_with("channels/channels/4/", method="DELETE")

    await actions._delete("indexer", item_id=4)
    mock_handler.request.assert_called_with("indexer/4", method="DELETE")
