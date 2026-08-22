from unittest.mock import AsyncMock

import pytest

from pyarr._async.bazarr.episodes import Episodes
from pyarr._async.bazarr.movies import Movies
from pyarr._async.bazarr.subtitles import Subtitles
from pyarr._async.utils.http import RequestHandler


@pytest.mark.asyncio
async def test_subtitles_get():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    subtitles = Subtitles(mock_handler)

    assert await subtitles.get() == []
    mock_handler.request.assert_called_with("subtitles", params={})


def test_subtitles_has_no_per_id_actions():
    """Bazarr has no subtitles/{id} route; those actions belong to the media."""
    mock_handler = AsyncMock(spec=RequestHandler)
    subtitles = Subtitles(mock_handler)

    assert not hasattr(subtitles, "download")
    assert not hasattr(subtitles, "delete")


@pytest.mark.asyncio
async def test_episode_download_subtitle():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {}
    episodes = Episodes(mock_handler)

    await episodes.download_subtitle(series_id=7, episode_id=42, language="en")

    mock_handler.request.assert_called_with(
        "episodes/subtitles",
        method="PATCH",
        params={"seriesid": 7, "episodeid": 42, "language": "en", "forced": False, "hi": False},
    )


@pytest.mark.asyncio
async def test_episode_delete_subtitle():
    mock_handler = AsyncMock(spec=RequestHandler)
    episodes = Episodes(mock_handler)

    await episodes.delete_subtitle(series_id=7, episode_id=42, language="en", path="/tv/ep.en.srt", hi=True)

    mock_handler.request.assert_called_with(
        "episodes/subtitles",
        method="DELETE",
        params={
            "seriesid": 7,
            "episodeid": 42,
            "language": "en",
            "path": "/tv/ep.en.srt",
            "forced": False,
            "hi": True,
        },
    )


@pytest.mark.asyncio
async def test_movie_download_subtitle():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {}
    movies = Movies(mock_handler)

    await movies.download_subtitle(movie_id=3, language="fr", forced=True)

    mock_handler.request.assert_called_with(
        "movies/subtitles",
        method="PATCH",
        params={"radarrid": 3, "language": "fr", "forced": True, "hi": False},
    )


@pytest.mark.asyncio
async def test_movie_delete_subtitle():
    mock_handler = AsyncMock(spec=RequestHandler)
    movies = Movies(mock_handler)

    await movies.delete_subtitle(movie_id=3, language="fr", path="/movies/m.fr.srt")

    mock_handler.request.assert_called_with(
        "movies/subtitles",
        method="DELETE",
        params={"radarrid": 3, "language": "fr", "path": "/movies/m.fr.srt", "forced": False, "hi": False},
    )
