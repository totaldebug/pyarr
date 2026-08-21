"""Tests for the Bazarr series, movies and episodes endpoints (#189, #204)."""

from unittest.mock import AsyncMock, MagicMock, call

import httpx
import pytest

from pyarr._async.bazarr.episodes import Episodes as AsyncEpisodes
from pyarr._async.bazarr.movies import Movies as AsyncMovies
from pyarr._async.bazarr.providers import Providers as AsyncProviders
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


@pytest.mark.asyncio
async def test_async_providers_get():
    """Bazarr answers /api/providers with an enveloped object, not a bare list."""
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = {"data": []}
    providers = AsyncProviders(mock_handler)

    assert await providers.get() == {"data": []}
    mock_handler.request.assert_called_once_with("providers")


@pytest.mark.asyncio
async def test_async_providers_get_rejects_non_dict_response():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = []
    providers = AsyncProviders(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        await providers.get()


def test_series_run_action():
    """Bazarr takes the action and the series ID as query parameters on a PATCH (#204)."""
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    assert series.run_action("search-missing", series_id=101) is None
    mock_handler.request.assert_called_once_with(
        "series", method="PATCH", params={"action": "search-missing", "seriesid": 101}
    )


def test_series_run_action_scan_disk_and_sync():
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    series.run_action("scan-disk", series_id=101)
    series.run_action("sync", series_id=101)

    assert mock_handler.request.call_args_list == [
        call("series", method="PATCH", params={"action": "scan-disk", "seriesid": 101}),
        call("series", method="PATCH", params={"action": "sync", "seriesid": 101}),
    ]


def test_series_run_action_search_wanted_needs_no_id():
    """``search-wanted`` searches every wanted series, Bazarr ignores any ID given."""
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    assert series.run_action("search-wanted") is None
    mock_handler.request.assert_called_once_with("series", method="PATCH", params={"action": "search-wanted"})


def test_series_run_action_requires_a_series_id():
    """Bazarr answers an ID-less scan or sync with a 204 having done nothing, so fail loudly instead."""
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    with pytest.raises(PyarrMissingArgument, match="series_id must be provided"):
        series.run_action("scan-disk")

    mock_handler.request.assert_not_called()


def test_series_set_languages_profile():
    """The POST pairs ``seriesid`` and ``profileid`` by position, so both are sent as lists."""
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    assert series.set_languages_profile(101, 1) is None
    mock_handler.request.assert_called_once_with(
        "series", method="POST", params={"seriesid": [101], "profileid": [1]}
    )


def test_series_set_languages_profile_with_lists():
    """``"null"`` clears a profile, Bazarr rejects ``"none"`` despite what its own help text says."""
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    series.set_languages_profile([101, 102], [1, "null"])
    mock_handler.request.assert_called_once_with(
        "series", method="POST", params={"seriesid": [101, 102], "profileid": [1, "null"]}
    )


def test_series_set_languages_profile_rejects_mismatched_lengths():
    """Bazarr zips the two lists and 500s on a mismatch, so the pairing is checked up front."""
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    with pytest.raises(ValueError, match="same number of items"):
        series.set_languages_profile([101, 102], 1)

    mock_handler.request.assert_not_called()


def test_movies_run_action():
    mock_handler = MagicMock(spec=RequestHandler)
    movies = Movies(mock_handler)

    assert movies.run_action("search-missing", movie_id=201) is None
    mock_handler.request.assert_called_once_with(
        "movies", method="PATCH", params={"action": "search-missing", "radarrid": 201}
    )


def test_movies_run_action_search_wanted_needs_no_id():
    mock_handler = MagicMock(spec=RequestHandler)
    movies = Movies(mock_handler)

    assert movies.run_action("search-wanted") is None
    mock_handler.request.assert_called_once_with("movies", method="PATCH", params={"action": "search-wanted"})


def test_movies_run_action_requires_a_movie_id():
    mock_handler = MagicMock(spec=RequestHandler)
    movies = Movies(mock_handler)

    with pytest.raises(PyarrMissingArgument, match="movie_id must be provided"):
        movies.run_action("sync")

    mock_handler.request.assert_not_called()


def test_movies_set_languages_profile():
    mock_handler = MagicMock(spec=RequestHandler)
    movies = Movies(mock_handler)

    assert movies.set_languages_profile([201, 202], [1, "null"]) is None
    mock_handler.request.assert_called_once_with(
        "movies", method="POST", params={"radarrid": [201, 202], "profileid": [1, "null"]}
    )


def test_movies_set_languages_profile_rejects_mismatched_lengths():
    mock_handler = MagicMock(spec=RequestHandler)
    movies = Movies(mock_handler)

    with pytest.raises(ValueError, match="same number of items"):
        movies.set_languages_profile(201, [1, 2])

    mock_handler.request.assert_not_called()


def test_languages_profile_pairs_are_sent_in_order():
    """Bazarr pairs the repeated parameters by position, so the wire order has to be preserved."""
    request = httpx.Request(
        "POST",
        "http://localhost:6767/api/series",
        params={"seriesid": [101, 102], "profileid": [1, "null"]},
    )

    assert request.url.params.get_list("seriesid") == ["101", "102"]
    assert request.url.params.get_list("profileid") == ["1", "null"]


@pytest.mark.asyncio
async def test_async_series_run_action():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    series = AsyncSeries(mock_handler)

    assert await series.run_action("sync", series_id=101) is None
    mock_handler.request.assert_called_once_with("series", method="PATCH", params={"action": "sync", "seriesid": 101})


@pytest.mark.asyncio
async def test_async_series_run_action_search_wanted_needs_no_id():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    series = AsyncSeries(mock_handler)

    assert await series.run_action("search-wanted") is None
    mock_handler.request.assert_called_once_with("series", method="PATCH", params={"action": "search-wanted"})


@pytest.mark.asyncio
async def test_async_series_run_action_requires_a_series_id():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    series = AsyncSeries(mock_handler)

    with pytest.raises(PyarrMissingArgument, match="series_id must be provided"):
        await series.run_action("search-missing")

    mock_handler.request.assert_not_called()


@pytest.mark.asyncio
async def test_async_series_set_languages_profile():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    series = AsyncSeries(mock_handler)

    assert await series.set_languages_profile([101, 102], [1, "null"]) is None
    mock_handler.request.assert_called_once_with(
        "series", method="POST", params={"seriesid": [101, 102], "profileid": [1, "null"]}
    )


@pytest.mark.asyncio
async def test_async_series_set_languages_profile_rejects_mismatched_lengths():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    series = AsyncSeries(mock_handler)

    with pytest.raises(ValueError, match="same number of items"):
        await series.set_languages_profile([101, 102], 1)

    mock_handler.request.assert_not_called()


@pytest.mark.asyncio
async def test_async_movies_run_action():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    movies = AsyncMovies(mock_handler)

    assert await movies.run_action("scan-disk", movie_id=201) is None
    mock_handler.request.assert_called_once_with(
        "movies", method="PATCH", params={"action": "scan-disk", "radarrid": 201}
    )


@pytest.mark.asyncio
async def test_async_movies_run_action_search_wanted_needs_no_id():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    movies = AsyncMovies(mock_handler)

    assert await movies.run_action("search-wanted") is None
    mock_handler.request.assert_called_once_with("movies", method="PATCH", params={"action": "search-wanted"})


@pytest.mark.asyncio
async def test_async_movies_run_action_requires_a_movie_id():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    movies = AsyncMovies(mock_handler)

    with pytest.raises(PyarrMissingArgument, match="movie_id must be provided"):
        await movies.run_action("scan-disk")

    mock_handler.request.assert_not_called()


@pytest.mark.asyncio
async def test_async_movies_set_languages_profile():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    movies = AsyncMovies(mock_handler)

    assert await movies.set_languages_profile(201, 1) is None
    mock_handler.request.assert_called_once_with(
        "movies", method="POST", params={"radarrid": [201], "profileid": [1]}
    )


@pytest.mark.asyncio
async def test_async_movies_set_languages_profile_rejects_mismatched_lengths():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    movies = AsyncMovies(mock_handler)

    with pytest.raises(ValueError, match="same number of items"):
        await movies.set_languages_profile(201, [1, 2])

    mock_handler.request.assert_not_called()
