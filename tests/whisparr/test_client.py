import pytest

from pyarr._async.common.config import MediaConfig
from pyarr._async.sonarr.episode import Episode
from pyarr._async.sonarr.episode_file import EpisodeFile
from pyarr._async.sonarr.manual_import import ManualImport
from pyarr._async.sonarr.release import Release
from pyarr._async.sonarr.series import Series
from pyarr._async.whisparr import Whisparr


@pytest.fixture()
def whisparr_client():
    return Whisparr(host="127.0.0.1", api_key="123456789abcdefg123456789", tls=False, api_ver="v3")


def test_whisparr_uses_the_sonarr_library_components(whisparr_client):
    """Whisparr V2 forks Sonarr v3, so its library is series and episodes."""
    assert isinstance(whisparr_client.series, Series)
    assert isinstance(whisparr_client.episode, Episode)
    assert isinstance(whisparr_client.episode_file, EpisodeFile)
    assert isinstance(whisparr_client.release, Release)
    assert isinstance(whisparr_client.manual_import, ManualImport)


def test_whisparr_no_longer_exposes_the_radarr_movie_components(whisparr_client):
    """movie, movie/lookup, movie/editor and moviefile all return 404 on this fork."""
    assert not hasattr(whisparr_client, "movie")
    assert not hasattr(whisparr_client, "movie_file")


def test_whisparr_config_is_implemented(whisparr_client):
    """The client previously attached an empty Config class with no methods at all."""
    assert isinstance(whisparr_client.config, MediaConfig)
    for method in ("get_host", "get_ui", "get_naming", "get_media_management", "get_indexer"):
        assert hasattr(whisparr_client.config, method)


def test_whisparr_series_targets_the_series_endpoint(whisparr_client):
    """A cheap guard that the reused component really is series-shaped, not movie-shaped."""
    import inspect

    source = inspect.getsource(type(whisparr_client.series))
    assert '"series"' in source
    assert '"movie"' not in source
