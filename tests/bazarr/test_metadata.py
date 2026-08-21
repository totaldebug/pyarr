"""Tests for the Bazarr series, movies and episodes endpoints (#189)."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from pyarr._async.bazarr.episodes import Episodes as AsyncEpisodes
from pyarr._async.bazarr.movies import Movies as AsyncMovies
from pyarr._async.bazarr.series import Series as AsyncSeries
from pyarr._async.utils.http import RequestHandler as AsyncRequestHandler
from pyarr._sync.bazarr.episodes import Episodes
from pyarr._sync.bazarr.providers import Providers
from pyarr._sync.bazarr.movies import Movies
from pyarr._sync.bazarr.series import Series
from pyarr._sync.utils.http import RequestHandler
from pyarr.exceptions import PyarrMissingArgument

SERIES_RESPONSE = {"data": [{"sonarrSeriesId": 101, "title": "Series One"}], "total": 1}
MOVIES_RESPONSE = {"data": [{"radarrId": 201, "title": "Movie One"}], "total": 1}
EPISODES_RESPONSE = {"data": [{"sonarrEpisodeId": 5001, "sonarrSeriesId": 101, "title": "One S01E01"}]}


def test_series_get():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = SERIES_RESPONSE
    series = Series(mock_handler)

    assert series.get() == SERIES_RESPONSE
    mock_handler.request.assert_called_once_with("series", params={})


def test_series_get_with_series_id_list():
    """A list of IDs is sent under the literal ``seriesid[]`` key so httpx repeats it per value."""
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = SERIES_RESPONSE
    series = Series(mock_handler)

    series.get(series_id=[101, 102])
    mock_handler.request.assert_called_once_with("series", params={"seriesid[]": [101, 102]})


def test_series_get_with_single_series_id_and_kwargs():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = SERIES_RESPONSE
    series = Series(mock_handler)

    series.get(series_id=101, start=0, length=10)
    mock_handler.request.assert_called_once_with("series", params={"start": 0, "length": 10, "seriesid[]": 101})


def test_series_get_rejects_non_dict_response():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    series = Series(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        series.get()


def test_movies_get():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = MOVIES_RESPONSE
    movies = Movies(mock_handler)

    assert movies.get() == MOVIES_RESPONSE
    mock_handler.request.assert_called_once_with("movies", params={})


def test_movies_get_with_movie_id_list():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = MOVIES_RESPONSE
    movies = Movies(mock_handler)

    movies.get(movie_id=[201, 202])
    mock_handler.request.assert_called_once_with("movies", params={"radarrid[]": [201, 202]})


def test_movies_get_rejects_non_dict_response():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    movies = Movies(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        movies.get()


def test_episodes_get_with_series_id_list():
    """``seriesid[]`` takes a list of series IDs, sent as a repeated query parameter."""
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = EPISODES_RESPONSE
    episodes = Episodes(mock_handler)

    assert episodes.get(series_id=[101, 102]) == EPISODES_RESPONSE
    mock_handler.request.assert_called_once_with("episodes", params={"seriesid[]": [101, 102]})


def test_episodes_get_with_single_series_id():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = EPISODES_RESPONSE
    episodes = Episodes(mock_handler)

    episodes.get(series_id=101)
    mock_handler.request.assert_called_once_with("episodes", params={"seriesid[]": 101})


def test_episodes_get_with_episode_id():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = EPISODES_RESPONSE
    episodes = Episodes(mock_handler)

    episodes.get(episode_id=[5001, 5002])
    mock_handler.request.assert_called_once_with("episodes", params={"episodeid[]": [5001, 5002]})


def test_episodes_get_requires_an_id():
    """Bazarr answers an unfiltered episodes request with a 404, so fail before the request."""
    mock_handler = MagicMock(spec=RequestHandler)
    episodes = Episodes(mock_handler)

    with pytest.raises(PyarrMissingArgument):
        episodes.get()

    mock_handler.request.assert_not_called()


def test_episodes_get_requires_an_id_even_with_kwargs():
    """Other params must not satisfy the ID requirement - the request would still 404."""
    mock_handler = MagicMock(spec=RequestHandler)
    episodes = Episodes(mock_handler)

    with pytest.raises(PyarrMissingArgument):
        episodes.get(start=0, length=10)

    mock_handler.request.assert_not_called()


def test_episodes_get_rejects_non_dict_response():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    episodes = Episodes(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        episodes.get(series_id=101)


def test_seriesid_list_is_sent_as_a_repeated_parameter():
    """The transport must repeat ``seriesid[]`` once per ID, which is the form Bazarr parses."""
    request = httpx.Request("GET", "http://localhost:6767/api/episodes", params={"seriesid[]": [101, 102]})

    assert str(request.url) == "http://localhost:6767/api/episodes?seriesid%5B%5D=101&seriesid%5B%5D=102"
    assert request.url.params.get_list("seriesid[]") == ["101", "102"]


@pytest.mark.asyncio
async def test_async_series_get():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = SERIES_RESPONSE
    series = AsyncSeries(mock_handler)

    assert await series.get() == SERIES_RESPONSE
    mock_handler.request.assert_called_once_with("series", params={})


@pytest.mark.asyncio
async def test_async_series_get_with_series_id_list():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = SERIES_RESPONSE
    series = AsyncSeries(mock_handler)

    await series.get(series_id=[101, 102])
    mock_handler.request.assert_called_once_with("series", params={"seriesid[]": [101, 102]})


@pytest.mark.asyncio
async def test_async_series_get_rejects_non_dict_response():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = []
    series = AsyncSeries(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        await series.get()


@pytest.mark.asyncio
async def test_async_movies_get():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = MOVIES_RESPONSE
    movies = AsyncMovies(mock_handler)

    assert await movies.get() == MOVIES_RESPONSE
    mock_handler.request.assert_called_once_with("movies", params={})


@pytest.mark.asyncio
async def test_async_movies_get_with_movie_id_list():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = MOVIES_RESPONSE
    movies = AsyncMovies(mock_handler)

    await movies.get(movie_id=[201, 202])
    mock_handler.request.assert_called_once_with("movies", params={"radarrid[]": [201, 202]})


@pytest.mark.asyncio
async def test_async_movies_get_rejects_non_dict_response():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = []
    movies = AsyncMovies(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        await movies.get()


@pytest.mark.asyncio
async def test_async_episodes_get_with_series_id_list():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = EPISODES_RESPONSE
    episodes = AsyncEpisodes(mock_handler)

    assert await episodes.get(series_id=[101, 102]) == EPISODES_RESPONSE
    mock_handler.request.assert_called_once_with("episodes", params={"seriesid[]": [101, 102]})


@pytest.mark.asyncio
async def test_async_episodes_get_with_episode_id():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = EPISODES_RESPONSE
    episodes = AsyncEpisodes(mock_handler)

    await episodes.get(episode_id=5001)
    mock_handler.request.assert_called_once_with("episodes", params={"episodeid[]": 5001})


@pytest.mark.asyncio
async def test_async_episodes_get_requires_an_id():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    episodes = AsyncEpisodes(mock_handler)

    with pytest.raises(PyarrMissingArgument):
        await episodes.get()

    mock_handler.request.assert_not_called()


@pytest.mark.asyncio
async def test_async_episodes_get_rejects_non_dict_response():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = []
    episodes = AsyncEpisodes(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        await episodes.get(series_id=101)


def test_providers_get():
    """Bazarr answers /api/providers with an enveloped object, not a bare list."""
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = {"data": []}
    providers = Providers(mock_handler)

    assert providers.get() == {"data": []}
    mock_handler.request.assert_called_once_with("providers")


def test_providers_get_rejects_non_dict_response():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    providers = Providers(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        providers.get()
