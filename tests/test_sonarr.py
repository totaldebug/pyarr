import contextlib
from datetime import datetime

import pytest

from pyarr.exceptions import (
    PyarrMissingArgument,
    PyarrRecordNotFound,
    PyarrResourceNotFound,
)
from pyarr.models.common import (
    PyarrHistorySortKey,
    PyarrLogFilterKey,
    PyarrLogFilterValue,
    PyarrLogSortKey,
    PyarrNotificationSchema,
    PyarrSortDirection,
    PyarrTaskSortKey,
)
from pyarr.models.sonarr import SonarrCommands, SonarrSortKey

from tests import load_fixture


@pytest.mark.usefixtures
def test__series_json(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series/lookup?term=tvdb%3A1234567",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series_lookup.json"),
        status=200,
        match_querystring=True,
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
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.get_command(4327826)
    assert isinstance(data, dict)

    # when an incorrect ID is supplied, not found response
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/command/4321",
        headers={"Content-Type": "application/json"},
        status=404,
        match_querystring=True,
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
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.get_episode(0)

    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode?seriesId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episode_series.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_episode(1, True)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode/999",
        headers={"Content-Type": "application/json"},
        status=404,
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.get_episodes_by_series_id(1)

    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode?seriesId=999",
        headers={"Content-Type": "application/json"},
        status=404,
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.get_episode_by_episode_id(0)

    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode/999",
        headers={"Content-Type": "application/json"},
        status=404,
        match_querystring=True,
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
        status=202,
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.get_episode_files_by_series_id(1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile?seriesId=999",
        headers={"Content-Type": "application/json"},
        status=404,
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.get_episode_file(0)

    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile?seriesId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episodefile_series.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_episode_file(1, True)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile/999",
        headers={"Content-Type": "application/json"},
        status=404,
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.del_episode_file(1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/episodefile/999",
        headers={"Content-Type": "application/json"},
        status=404,
        match_querystring=True,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.del_episode_file(999)
        assert False


@pytest.mark.usefixtures
def test_upd_episode_file_quality(responses, sonarr_client):
    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/episodefile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episodefile.json"),
        status=202,
        match_querystring=True,
    )
    data = sonarr_client.upd_episode_file_quality(
        1, load_fixture("sonarr/file_quality.json")
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_wanted(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/wanted/missing",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/wanted_missing.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_wanted()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/wanted/missing?includeSeries=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/wanted_missing_extended.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_wanted(include_series=True)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/wanted/missing?page=2&pageSize=20&sortKey=series.sortTitle&sortDirection=ascending",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/wanted_missing.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_wanted(
        page=2,
        page_size=20,
        sort_key=SonarrSortKey.SERIES_TITLE,
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
        match_querystring=True,
    )
    data = sonarr_client.get_quality_profile()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualityprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/qualityprofile.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_quality_profile(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_queue(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/queue",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_queue()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/queue?page=1&pageSize=20&sortKey=timeleft&sortDirection=default&includeUnknownSeriesItems=False&includeSeries=False&includeEpisode=False",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_queue(
        page=1,
        page_size=20,
        sort_key=SonarrSortKey.TIMELEFT,
        sort_dir=PyarrSortDirection.DEFAULT,
        include_unknown_series_items=False,
        include_series=False,
        include_episode=False,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_queue(sort_key=SonarrSortKey.TIMELEFT)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_queue(sort_dir=PyarrSortDirection.DEFAULT)
        assert False


@pytest.mark.usefixtures
def test_get_parsed_title(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/parse?title=Series.Title.S01E01",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/parse.json"),
        status=200,
        match_querystring=True,
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
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.get_parse_title_path(title="Series.Title.S01E01", path="/")
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/parse?title=Series.Title.S01E01",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/parse.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_parse_title_path(title="Series.Title.S01E01")
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/parse?path=/",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/parse.json"),
        status=200,
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.get_releases()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/release?episodeId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/release.json"),
        status=200,
        match_querystring=True,
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
        match_querystring=True,
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
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.get_series()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_series(1)
    assert isinstance(data, dict)


def test_add_series(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series/lookup?term=tvdb:123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series_lookup.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.POST,
        "https://127.0.0.1:8989/api/v3/series",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.add_series(tvdb_id=123456, quality_profile_id=0, root_dir="/")
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_series(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series.json"),
        status=202,
        match_querystring=True,
    )
    series = sonarr_client.get_series(1)
    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/series",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series.json"),
        status=202,
        match_querystring=True,
    )
    data = sonarr_client.upd_series(data=series)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_del_series(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/series/1?deleteFiles=False",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
        match_querystring=True,
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
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.lookup_series(id_=123456)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/series/lookup?term=test",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series_lookup.json"),
        status=200,
        match_querystring=True,
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
        match_querystring=True,
    )
    data = sonarr_client.lookup_series_by_tvdb_id(123456)
    assert isinstance(data, list)


#### BASE TESTS ####
# These  tests are to make sure the base functions work as
# expected for each api


@pytest.mark.usefixtures
def test_get_calendar(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/calendar?start=2020-11-30&end=2020-12-01&unmonitored=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/calendar.json"),
        status=200,
        match_querystring=True,
    )
    start = datetime.strptime("Nov 30 2020  1:33PM", "%b %d %Y %I:%M%p")
    end = datetime.strptime("Dec 1 2020  1:33PM", "%b %d %Y %I:%M%p")
    data = sonarr_client.get_calendar(start_date=start, end_date=end)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/calendar?start=2020-11-30&end=2020-12-01&unmonitored=False",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/calendar.json"),
        status=200,
        match_querystring=True,
    )
    start = datetime.strptime("Nov 30 2020  1:33PM", "%b %d %Y %I:%M%p")
    end = datetime.strptime("Dec 1 2020  1:33PM", "%b %d %Y %I:%M%p")
    data = sonarr_client.get_calendar(start_date=start, end_date=end, unmonitored=False)
    assert isinstance(data, list)


def test_get_system_status(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/system/status",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/system_status.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_system_status()
    assert isinstance(data, dict)


def test_get_health(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/health",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/health.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_health()
    assert isinstance(data, list)


def test_get_metadata(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/metadata",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/metadata_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_metadata()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/metadata/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/metadata.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_metadata(1)
    assert isinstance(data, dict)


def test_get_update(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/update",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/metadata_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_update()
    assert isinstance(data, list)


def test_get_root_folder(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/rootfolder",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/rootfolder_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_root_folder()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/rootfolder/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/rootfolder.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_root_folder(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_del_root_folder(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/rootfolder/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.del_root_folder(1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/rootfolder/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.del_root_folder(999)
        assert False


@pytest.mark.usefixtures
def test_get_disk_space(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/diskspace",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/diskspace.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_disk_space()
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_backup(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/system/backup",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/backup.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_backup()
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_log(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/log",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/log.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_log()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/log?page=10&pageSize=10&sortKey=Id&sortDirection=descending",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/log.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_log(
        page=10,
        page_size=10,
        sort_key=PyarrLogSortKey.ID,
        sort_dir=PyarrSortDirection.DESC,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_log(sort_key=PyarrLogSortKey.ID)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_log(sort_dir=PyarrSortDirection.DESC)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_log(filter_key=PyarrLogFilterKey.LEVEL)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_log(filter_value=PyarrLogFilterValue.ALL)
        assert False


@pytest.mark.usefixtures
def test_get_history(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/history",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/history.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_history()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/history?episodeId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/history.json"),
        status=200,
        match_querystring=True,
    )

    data = sonarr_client.get_history(id_=1)
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_history(sort_key=PyarrHistorySortKey.TIME)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_history(sort_dir=PyarrSortDirection.DESC)
        assert False


@pytest.mark.usefixtures
def test_get_blocklist(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/blocklist",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/blocklist.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_blocklist()
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_blocklist(sort_key=PyarrHistorySortKey.TIME)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_blocklist(sort_dir=PyarrSortDirection.DESC)
        assert False


@pytest.mark.usefixtures
def test_del_blocklist(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/blocklist/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.del_blocklist(1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/blocklist/999",
        headers={"Content-Type": "application/json"},
        status=404,
        match_querystring=True,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.del_blocklist(999)
        assert False


@pytest.mark.usefixtures
def test_del_blocklist_bulk(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/blocklist/bulk",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.del_blocklist_bulk(ids=[8])
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_quality_profile(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualityprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/quality_profile_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_quality_profile()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualityprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/quality_profile.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_quality_profile(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_quality_profile(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualityprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/quality_profile.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_quality_profile(1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/qualityprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/quality_profile.json"),
        status=202,
        match_querystring=True,
    )
    data = sonarr_client.upd_quality_profile(1, data)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_del_quality_profile(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/qualityprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.del_quality_profile(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_quality_definition(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualitydefinition",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/quality_definition_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_quality_definition()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualitydefinition/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/quality_definition.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_quality_definition(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_quality_definition(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualitydefinition/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/quality_definition.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_quality_definition(1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/qualitydefinition/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/quality_definition.json"),
        status=202,
        match_querystring=True,
    )
    data = sonarr_client.upd_quality_definition(1, data)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_indexer(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/indexer",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/indexer_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_indexer()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/indexer.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_indexer(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_indexer(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/indexer.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_indexer(1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/indexer.json"),
        status=202,
        match_querystring=True,
    )
    data = sonarr_client.upd_indexer(1, data)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_del_indexer(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.del_indexer(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_del_queue(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/queue/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.del_queue(id_=1)
    assert isinstance(data, dict)
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/queue/1?removeFromClient=True&blacklist=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.del_queue(id_=1, remove_from_client=True, blacklist=True)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_task(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/system/task",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/system_task_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_task()
    assert isinstance(data, dict)

    # TODO: Need an example task, currently using fake dict
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/system/task/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/system_task.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_task(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/system/task?page=1&pageSize=10&sortKey=timeleft&sortDirection=default",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/system_task_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_task(
        page=1,
        page_size=10,
        sort_key=PyarrTaskSortKey.TIME_LEFT,
        sort_dir=PyarrSortDirection.DEFAULT,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_task(sort_key=PyarrTaskSortKey.TIME_LEFT)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_task(sort_dir=PyarrSortDirection.DESC)
        assert False


@pytest.mark.usefixtures
def test_get_remote_path_mapping(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/remotepathmapping",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/remotepathmapping_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_remote_path_mapping()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/remotepathmapping/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/remotepathmapping.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_remote_path_mapping(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_config_ui(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/config/ui",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/config_ui.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_config_ui()
    assert isinstance(data, dict)


# TODO: update config ui


@pytest.mark.usefixtures
def test_get_config_host(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/config/host",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/config_host.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_config_host()
    assert isinstance(data, dict)


# TODO: update config host


@pytest.mark.usefixtures
def test_get_config_naming(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/config/naming",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/config_naming.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_config_naming()
    assert isinstance(data, dict)


# TODO: update config naming


@pytest.mark.usefixtures
def test_get_media_management(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/config/mediamanagement",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/media_management.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_media_management()
    assert isinstance(data, dict)


# TODO: update media management


@pytest.mark.usefixtures
def test_get_notification(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/notification",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/notification_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_notification()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/notification/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/notification.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_notification(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_notification_schema(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/notification/schema",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/notification_schema_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_notification_schema()
    assert isinstance(data, list)

    data = sonarr_client.get_notification_schema(
        implementation=PyarrNotificationSchema.BOXCAR
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrRecordNotFound):
        data = sonarr_client.get_notification_schema(implementation="polarbear")
        assert False


# TODO: update notification


@pytest.mark.usefixtures
def test_del_notification(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/notification/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.del_notification(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_tag(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/tag",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/tag_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_tag()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/tag/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/tag.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_tag(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_tag_detail(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/tag/detail",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/tag_detail_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_tag_detail()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/tag/detail/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/tag_detail.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_tag_detail(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_create_tag(responses, sonarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8989/api/v3/tag",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/tag.json"),
        status=201,
        match_querystring=True,
    )
    data = sonarr_client.create_tag(label="string")
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_tag(responses, sonarr_client):
    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/tag",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/tag.json"),
        status=202,
        match_querystring=True,
    )
    data = sonarr_client.upd_tag(id_=1, label="string")
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_del_tag(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/tag/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.del_tag(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_download_client(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/downloadclient",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/downloadclient_all.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_download_client()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/downloadclient/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/downloadclient.json"),
        status=200,
        match_querystring=True,
    )
    data = sonarr_client.get_download_client(id_=1)
    assert isinstance(data, dict)
