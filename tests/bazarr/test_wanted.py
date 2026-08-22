from unittest.mock import AsyncMock

import pytest

from pyarr._async.bazarr.wanted import BazarrWanted
from pyarr._async.utils.http import RequestHandler


@pytest.mark.asyncio
async def test_bazarr_wanted_pages_with_start_and_length():
    """Bazarr declares only start, length and the id list. Flask-RestX drops anything else,
    so the Servarr page/pageSize parameters paged nothing at all."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"data": [], "total": 0}
    wanted = BazarrWanted(mock_handler, path="episodes/wanted")

    response = await wanted.get(start=10, length=25)

    assert response == {"data": [], "total": 0}
    mock_handler.request.assert_called_with("episodes/wanted", params={"start": 10, "length": 25})


@pytest.mark.asyncio
async def test_bazarr_wanted_start_zero_is_sent():
    """start=0 is a meaningful value and must not be dropped as falsy."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"data": [], "total": 0}
    wanted = BazarrWanted(mock_handler, path="movies/wanted")

    await wanted.get(start=0)

    mock_handler.request.assert_called_with("movies/wanted", params={"start": 0})


@pytest.mark.asyncio
async def test_bazarr_wanted_no_params():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"data": [], "total": 0}
    wanted = BazarrWanted(mock_handler, path="episodes/wanted")

    await wanted.get()

    mock_handler.request.assert_called_with("episodes/wanted", params={})


@pytest.mark.asyncio
async def test_bazarr_wanted_extra_params():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"data": [], "total": 0}
    wanted = BazarrWanted(mock_handler, path="episodes/wanted")

    await wanted.get(**{"episodeid[]": [1, 2]})

    mock_handler.request.assert_called_with("episodes/wanted", params={"episodeid[]": [1, 2]})


@pytest.mark.asyncio
async def test_bazarr_wanted_rejects_non_dict_response():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    wanted = BazarrWanted(mock_handler, path="episodes/wanted")

    with pytest.raises(TypeError):
        await wanted.get()
