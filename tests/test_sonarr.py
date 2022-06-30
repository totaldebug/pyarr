import contextlib
from datetime import datetime
from warnings import warn

import pytest

from pyarr.exceptions import (
    PyarrMissingArgument,
    PyarrRecordNotFound,
    PyarrResourceNotFound,
)
from pyarr.models.common import PyarrSortDirection
from pyarr.models.sonarr import SonarrCommands, SonarrSortKeys

from tests import load_fixture


@pytest.mark.usefixtures
def test__series_json(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series/lookup?term=tvdb%3A1234567",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series_lookup.json"),
        status=200,
    )

    data = sonarr_client._series_json(
        tvdb_id=1234567,
        quality_profile_id=1,
        root_dir="/",
        season_folder=False,
        monitored=False,
        ignore_episodes_with_files=True,
        ignore_episodes_without_files=True,
        search_for_missing_episodes=True,
    )

    assert isinstance(data, dict)
    assert data["rootFolderPath"] == "/"
    assert data["qualityProfileId"] == 1
    assert data["seasonFolder"] == False
    assert data["monitored"] == False
    assert data["tvdbId"] == 1234567
    assert data["addOptions"]["ignoreEpisodesWithFiles"] == True
    assert data["addOptions"]["ignoreEpisodesWithoutFiles"] == True
    assert data["addOptions"]["searchForMissingEpisodes"] == True


@pytest.mark.usefixtures
def test_get_command(responses, sonarr_client):
    """Check get_command()"""

    # No args
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/command",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/command_all.json"),
        status=200,
    )
    data = sonarr_client.get_command()
    assert isinstance(data, list)

    # When an ID is supplied
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/command/4327826",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/command.json"),
        status=200,
    )
    data = sonarr_client.get_command(4327826)
    assert isinstance(data, dict)

    # when an incorrect ID is supplied, not found response
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/command/4321",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.get_command(4321)
        assert False


@pytest.mark.usefixtures
def test_post_command(responses, sonarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8989/api/v3/command",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/command.json"),
        status=201,
    )

    data = sonarr_client.post_command(name=SonarrCommands.REFRESH_SERIES)
    assert isinstance(data, dict)
    data = sonarr_client.post_command(SonarrCommands.REFRESH_SERIES, seriesId=1)
    assert isinstance(data, dict)
    data = sonarr_client.post_command(SonarrCommands.RESCAN_SERIES)
    assert isinstance(data, dict)
    data = sonarr_client.post_command(SonarrCommands.RESCAN_SERIES, seriesId=1)
    assert isinstance(data, dict)
    data = sonarr_client.post_command(
        SonarrCommands.EPISODE_SEARCH, episodeIds=[1, 2, 3]
    )
    assert isinstance(data, dict)
    data = sonarr_client.post_command(
        SonarrCommands.SEASON_SEARCH, seriesId=1, seasonNumber=1
    )
    assert isinstance(data, dict)
    data = sonarr_client.post_command(SonarrCommands.SERIES_SEARCH, seriesId=1)
    assert isinstance(data, dict)
    data = sonarr_client.post_command(SonarrCommands.DOWNLOADED_EPISODES_SCAN)
    assert isinstance(data, dict)
    data = sonarr_client.post_command(SonarrCommands.RSS_SYNC)
    assert isinstance(data, dict)
    data = sonarr_client.post_command(SonarrCommands.RENAME_FILES, files=[1, 2, 3])
    assert isinstance(data, dict)
    data = sonarr_client.post_command(SonarrCommands.RENAME_SERIES, seriesIds=[1, 2, 3])
    assert isinstance(data, dict)
    data = sonarr_client.post_command(SonarrCommands.BACKUP)
    assert isinstance(data, dict)

    data = sonarr_client.post_command(SonarrCommands.MISSING_EPISODE_SEARCH)


@pytest.mark.usefixtures
def test_get_episode(responses, sonarr_client):
    """Test getting episode"""
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode/0",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episode.json"),
        status=200,
    )
    data = sonarr_client.get_episode(0)

    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode?seriesId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episode_series.json"),
        status=200,
    )
    data = sonarr_client.get_episode(1, True)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.get_episode(999)
        assert False


@pytest.mark.usefixtures
def test_get_episodes_by_series_id(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode?seriesId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episode_series.json"),
        status=200,
    )
    data = sonarr_client.get_episodes_by_series_id(1)

    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode?seriesId=999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.get_episodes_by_series_id(999)
        assert False


@pytest.mark.usefixtures
def test_get_episode_by_episode_id(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode/0",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episode.json"),
        status=200,
    )
    data = sonarr_client.get_episode_by_episode_id(0)

    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.get_episode_by_episode_id(999)
        assert False


@pytest.mark.usefixtures
def test_upd_episode(responses, sonarr_client):
    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/episode/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episode_update.json"),
        status=200,
    )
    payload = {"monitored": True}
    data = sonarr_client.upd_episode(1, payload)

    assert isinstance(data, dict)
    assert data["monitored"] == True

    # TODO: Add test if incorrect data provided


@pytest.mark.usefixtures
def test_get_episode_files_by_series_id(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile?seriesId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episodefile_series.json"),
        status=200,
    )
    data = sonarr_client.get_episode_files_by_series_id(1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile?seriesId=999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.get_episode_files_by_series_id(999)
        assert False


@pytest.mark.usefixtures
def test_get_episode_file(responses, sonarr_client):
    """Test getting episode"""
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile/0",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episodefile.json"),
        status=200,
    )
    data = sonarr_client.get_episode_file(0)

    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile?seriesId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episodefile_series.json"),
        status=200,
    )
    data = sonarr_client.get_episode_file(1, True)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.get_episode_file(999)
        assert False


@pytest.mark.usefixtures
def test_del_episode_file(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/episodefile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
    )
    data = sonarr_client.del_episode_file(1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/episodefile/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.del_episode_file(999)
        assert False


@pytest.mark.usefixtures
def test_get_wanted(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/wanted/missing?sortKey=airDateUtc&page=1&pageSize=10&sortDirection=default",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/wanted_missing.json"),
        status=200,
    )
    data = sonarr_client.get_wanted()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/wanted/missing?sortKey=airDateUtc&page=1&pageSize=10&sortDirection=default&includeSeries=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/wanted_missing_extended.json"),
        status=200,
    )
    data = sonarr_client.get_wanted(include_series=True)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/wanted/missing?sortKey=series.sortTitle&page=2&pageSize=20&sortDirection=ascending",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/wanted_missing.json"),
        status=200,
    )
    data = sonarr_client.get_wanted(
        sort_key=SonarrSortKeys.SERIES_TITLE,
        page=2,
        page_size=20,
        sort_dir=PyarrSortDirection.ASC,
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_quality_profile(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualityprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/qualityprofileall.json"),
        status=200,
    )
    data = sonarr_client.get_quality_profile()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualityprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/qualityprofile.json"),
        status=200,
    )
    data = sonarr_client.get_quality_profile(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_queue(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/queue?page=1&pageSize=20&sortDirection=default&sortKey=timeleft&includeUnknownSeriesItems=False&includeSeries=False&includeEpisode=False",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/queue.json"),
        status=200,
    )
    data = sonarr_client.get_queue()
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_parsed_title(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/parse?title=Series.Title.S01E01",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/parse.json"),
        status=200,
    )
    data = sonarr_client.get_parsed_title("Series.Title.S01E01")
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_parsed_path(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/parse?path=/",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/parse.json"),
        status=200,
    )
    data = sonarr_client.get_parsed_path("/")
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_parse_title_path(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/parse?title=Series.Title.S01E01&path=/",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/parse.json"),
        status=200,
    )
    data = sonarr_client.get_parse_title_path(title="Series.Title.S01E01", path="/")
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/parse?title=Series.Title.S01E01",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/parse.json"),
        status=200,
    )
    data = sonarr_client.get_parse_title_path(title="Series.Title.S01E01")
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/parse",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/parse.json"),
        status=200,
    )
    data = sonarr_client.get_parse_title_path(path="/")
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_parse_title_path()
        assert False


@pytest.mark.usefixtures
def test_get_releases(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/release",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/release.json"),
        status=200,
    )
    data = sonarr_client.get_releases()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/release?episodeId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/release.json"),
        status=200,
    )
    data = sonarr_client.get_releases(1)
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_download_release(responses, sonarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8989/api/v3/release",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/release_download.json"),
        status=201,
    )
    data = sonarr_client.download_release(guid="1450590", indexer_id=2)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_push_release(responses, sonarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8989/api/v3/release/push",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/release_download.json"),
        status=201,
    )
    data = sonarr_client.push_release(
        title="test",
        download_url="https://ipt.beelyrics.net/t/1450590",
        protocol="Torrent",
        publish_date=datetime(2020, 5, 17),
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_series(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series_all.json"),
        status=200,
    )
    data = sonarr_client.get_series()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series.json"),
        status=200,
    )
    data = sonarr_client.get_series(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_del_series(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/series/1?deleteFiles=False",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
    )
    data = sonarr_client.del_series(1)
    assert isinstance(data, dict)
    assert data == {}

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/series/1?deleteFiles=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
    )
    data = sonarr_client.del_series(1, delete_files=True)
    assert isinstance(data, dict)
    assert data == {}


@pytest.mark.usefixtures
def test_lookup_series(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series/lookup?term=tvdb:123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series_lookup.json"),
        status=200,
    )
    data = sonarr_client.lookup_series(id_=123456)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series/lookup?term=test",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series_lookup.json"),
        status=200,
    )
    data = sonarr_client.lookup_series(term="test")
    assert isinstance(data, list)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.lookup_series()
        assert False


@pytest.mark.usefixtures
def test_lookup_series_by_tvdb_id(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series/lookup?term=tvdb%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series_lookup.json"),
        status=200,
    )
    data = sonarr_client.lookup_series_by_tvdb_id(123456)
    assert isinstance(data, list)
