from unittest.mock import AsyncMock

import pytest

from pyarr._async.common.wanted import Wanted
from pyarr._async.utils.http import RequestHandler
from pyarr.exceptions import PyarrMissingArgument


@pytest.mark.asyncio
async def test_wanted_get():
    mock_handler = AsyncMock(spec=RequestHandler)
    wanted = Wanted(mock_handler)

    # Mock successful response
    mock_handler.request.return_value = {"records": [], "page": 1, "pageSize": 10}

    # Test basic get
    response = await wanted.get(page=1, page_size=10)
    assert isinstance(response, dict)
    assert response["page"] == 1
    mock_handler.request.assert_called_with("wanted/missing", params={"page": 1, "pageSize": 10})

    # Test with sort
    await wanted.get(sort_key="title", sort_dir="ascending")
    mock_handler.request.assert_called_with("wanted/missing", params={"sortKey": "title", "sortDirection": "ascending"})

    # Test with kwargs
    await wanted.get(includeSeries=True)
    mock_handler.request.assert_called_with("wanted/missing", params={"includeSeries": True})

    # Test missing sort argument
    with pytest.raises(PyarrMissingArgument):
        await wanted.get(sort_key="title")

    with pytest.raises(PyarrMissingArgument):
        await wanted.get(sort_dir="ascending")


@pytest.mark.asyncio
async def test_wanted_custom_path():
    mock_handler = AsyncMock(spec=RequestHandler)
    wanted = Wanted(mock_handler, path="subtitles/wanted")

    mock_handler.request.return_value = {"records": []}
    await wanted.get()
    mock_handler.request.assert_called_with("subtitles/wanted", params={})
