from unittest.mock import AsyncMock, MagicMock

import pytest

from pyarr._async.radarr.movie import Movie as AsyncMovie
from pyarr._async.utils.http import RequestHandler as AsyncRequestHandler
from pyarr._sync.radarr.movie import Movie
from pyarr._sync.utils.http import RequestHandler


def test_movie_delete_single():
    """A single ID deletes via movie/{id}, which reads the flags from the query string."""
    mock_handler = MagicMock(spec=RequestHandler)
    movie = Movie(mock_handler)

    movie.delete(1, delete_files=True, add_exclusion=True)

    mock_handler.request.assert_called_once_with(
        "movie/1",
        method="DELETE",
        params={"deleteFiles": True, "addImportExclusion": True},
    )


def test_movie_delete_single_defaults():
    mock_handler = MagicMock(spec=RequestHandler)
    movie = Movie(mock_handler)

    movie.delete(1)

    mock_handler.request.assert_called_once_with(
        "movie/1",
        method="DELETE",
        params={"deleteFiles": False, "addImportExclusion": False},
    )


def test_movie_delete_list_sends_flags_in_body():
    """Regression test for #190.

    movie/editor binds deleteFiles and addImportExclusion from the request body, so sending
    them as query parameters left the movie files on disk and skipped the list exclusion.
    """
    mock_handler = MagicMock(spec=RequestHandler)
    movie = Movie(mock_handler)

    movie.delete([1, 2], delete_files=True, add_exclusion=True)

    mock_handler.request.assert_called_once_with(
        "movie/editor",
        method="DELETE",
        json_data={"deleteFiles": True, "addImportExclusion": True, "movieIds": [1, 2]},
    )
    assert "params" not in mock_handler.request.call_args.kwargs


def test_movie_delete_list_defaults():
    mock_handler = MagicMock(spec=RequestHandler)
    movie = Movie(mock_handler)

    movie.delete([1])

    mock_handler.request.assert_called_once_with(
        "movie/editor",
        method="DELETE",
        json_data={"deleteFiles": False, "addImportExclusion": False, "movieIds": [1]},
    )


@pytest.mark.asyncio
async def test_async_movie_delete_single():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    movie = AsyncMovie(mock_handler)

    await movie.delete(1, delete_files=True, add_exclusion=True)

    mock_handler.request.assert_called_once_with(
        "movie/1",
        method="DELETE",
        params={"deleteFiles": True, "addImportExclusion": True},
    )


@pytest.mark.asyncio
async def test_async_movie_delete_list_sends_flags_in_body():
    """Regression test for #190, async client."""
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    movie = AsyncMovie(mock_handler)

    await movie.delete([1, 2], delete_files=True, add_exclusion=True)

    mock_handler.request.assert_called_once_with(
        "movie/editor",
        method="DELETE",
        json_data={"deleteFiles": True, "addImportExclusion": True, "movieIds": [1, 2]},
    )
    assert "params" not in mock_handler.request.call_args.kwargs
