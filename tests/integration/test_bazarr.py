import pytest

from pyarr import Bazarr
from pyarr.exceptions import PyarrBadRequest, PyarrMissingArgument, PyarrResourceNotFound


def test_bazarr_system_status(bazarr_client: Bazarr):
    status = bazarr_client.system.get_status()
    assert isinstance(status, dict)
    assert isinstance(status["data"], dict)


def test_bazarr_providers(bazarr_client: Bazarr):
    providers = bazarr_client.providers.get()
    assert isinstance(providers, dict)
    assert isinstance(providers["data"], list)


def test_bazarr_series(bazarr_client: Bazarr):
    series = bazarr_client.series.get()
    assert isinstance(series, dict)
    assert isinstance(series["data"], list)


def test_bazarr_movies(bazarr_client: Bazarr):
    movies = bazarr_client.movies.get()
    assert isinstance(movies, dict)
    assert isinstance(movies["data"], list)


def test_bazarr_episodes(bazarr_client: Bazarr):
    episodes = bazarr_client.episodes.get(series_id=[1, 2])
    assert isinstance(episodes, dict)
    assert isinstance(episodes["data"], list)


def test_bazarr_series_run_action(bazarr_client: Bazarr):
    """A successful action is a 204 with no body, so the call must simply come back without raising."""
    bazarr_client.series.run_action("search-wanted")
    bazarr_client.series.run_action("scan-disk", series_id=1)
    bazarr_client.series.run_action("sync", series_id=1)


def test_bazarr_movies_run_action(bazarr_client: Bazarr):
    bazarr_client.movies.run_action("search-wanted")
    bazarr_client.movies.run_action("scan-disk", movie_id=1)
    bazarr_client.movies.run_action("sync", movie_id=1)


def test_bazarr_patch_answers_204_from_the_real_route(bazarr_client: Bazarr):
    """Bazarr answers an unknown path with 200 and the SPA HTML (#192), so a 204 is the real route."""
    assert bazarr_client.http_utils.request("series", method="PATCH", params={"action": "search-wanted"}) is None
    assert bazarr_client.http_utils.request("movies", method="PATCH", params={"action": "search-wanted"}) is None

    spa = bazarr_client.http_utils.request("definitely-not-a-real-path")
    assert isinstance(spa, dict)
    assert "<!doctype html>" in spa["message"].lower()


def test_bazarr_series_run_action_rejects_an_unknown_action(bazarr_client: Bazarr):
    """Bazarr answers an unknown path with the SPA HTML page, so the 400 proves the real route ran."""
    with pytest.raises(PyarrBadRequest, match="Unknown action"):
        bazarr_client.series.run_action("not-an-action", series_id=1)  # type: ignore[arg-type]


def test_bazarr_movies_run_action_rejects_an_unknown_action(bazarr_client: Bazarr):
    with pytest.raises(PyarrBadRequest, match="Unknown action"):
        bazarr_client.movies.run_action("not-an-action", movie_id=1)  # type: ignore[arg-type]


def test_bazarr_run_action_requires_an_id(bazarr_client: Bazarr):
    """Bazarr would answer these with a 204 having done nothing, so pyarr fails before the request."""
    with pytest.raises(PyarrMissingArgument):
        bazarr_client.series.run_action("scan-disk")

    with pytest.raises(PyarrMissingArgument):
        bazarr_client.movies.run_action("sync")


def test_bazarr_series_set_languages_profile(bazarr_client: Bazarr):
    """``"null"`` clears the profile, Bazarr rejects ``"none"`` despite what its own help text says."""
    bazarr_client.series.set_languages_profile(1, "null")


def test_bazarr_movies_set_languages_profile(bazarr_client: Bazarr):
    bazarr_client.movies.set_languages_profile(1, "null")


def test_bazarr_set_languages_profile_rejects_an_unknown_profile(bazarr_client: Bazarr):
    with pytest.raises(PyarrResourceNotFound, match="Languages profile not found"):
        bazarr_client.series.set_languages_profile(1, "not-a-profile")
