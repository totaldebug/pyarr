import contextlib
from datetime import datetime
import random
import time

import pytest
import responses
from responses import matchers

from pyarr.exceptions import (
    PyarrMissingArgument,
    PyarrRecordNotFound,
    PyarrResourceNotFound,
)
from pyarr.sonarr import SonarrAPI

from tests import SONARR_TVDB, load_fixture


def test_add_root_folder(sonarr_client: SonarrAPI):
    data = sonarr_client.add_root_folder(directory="/defaults")
    assert isinstance(data, dict)


def test_get_root_folder(sonarr_client: SonarrAPI):
    data = sonarr_client.get_root_folder()
    assert isinstance(data, list)

    data = sonarr_client.get_root_folder(data[0]["id"])
    assert isinstance(data, dict)


def test_get_quality_profile(sonarr_client: SonarrAPI):
    data = sonarr_client.get_quality_profile()
    assert isinstance(data, list)

    data = sonarr_client.get_quality_profile(data[0]["id"])
    assert isinstance(data, dict)


def test_upd_quality_profile(sonarr_client: SonarrAPI):
    qual_profiles = sonarr_client.get_quality_profile()

    data = sonarr_client.upd_quality_profile(
        id_=qual_profiles[0]["id"], data=qual_profiles[0]
    )
    assert isinstance(data, dict)


def test_get_language_profile_schema(sonarr_client: SonarrAPI):
    data = sonarr_client.get_language_profile_schema()
    assert isinstance(data, dict)


def test_get_language_profile(sonarr_client: SonarrAPI):
    data = sonarr_client.get_language_profile()
    assert isinstance(data, list)

    data = sonarr_client.get_language_profile(data[0]["id"])
    assert isinstance(data, dict)

    with pytest.deprecated_call():
        sonarr_client.get_language_profile()


# def test_get_language(sonarr_client: SonarrAPI):
#    data = sonarr_client.get_language()
#    assert isinstance(data, list)
#
#    data = sonarr_client.get_language(data[0]["id"])
#    assert isinstance(data, dict)


def test_lookup_series(sonarr_client: SonarrAPI):
    data = sonarr_client.lookup_series(id_=SONARR_TVDB)
    assert isinstance(data, list)

    data = sonarr_client.lookup_series(term="Stranger Things")
    assert isinstance(data, list)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.lookup_series()
        assert False


def test_lookup_series_by_tvdb_id(sonarr_client: SonarrAPI):
    data = sonarr_client.lookup_series_by_tvdb_id(SONARR_TVDB)
    assert isinstance(data, list)

    with pytest.deprecated_call():
        sonarr_client.lookup_series_by_tvdb_id(SONARR_TVDB)


def test_add_series(sonarr_client: SonarrAPI):
    quality_profile = sonarr_client.get_quality_profile()
    language_profile = sonarr_client.get_language_profile()
    lookup_result = sonarr_client.lookup_series(id_=SONARR_TVDB)

    data = sonarr_client.add_series(
        series=lookup_result[0],
        quality_profile_id=quality_profile[0]["id"],
        language_profile_id=language_profile[0]["id"],
        root_dir="/defaults/",
    )
    assert isinstance(data, dict)
    assert data["title"] == "Stranger Things"

    with contextlib.suppress(Exception):
        data = sonarr_client.add_series(
            eries=lookup_result[0],
            quality_profile_id=quality_profile[0]["id"],
            language_profile_id=language_profile[0]["id"],
            root_dir="/defaults/",
        )
        assert False


def test_get_series(sonarr_client: SonarrAPI):
    data = sonarr_client.get_series()
    assert isinstance(data, list)

    data = sonarr_client.get_series(data[0]["id"])
    assert isinstance(data, dict)

    data = sonarr_client.get_series(id_=data["tvdbId"], tvdb=True)
    assert isinstance(data, list)


def test_get_episode(sonarr_client: SonarrAPI):
    """Test getting episode"""
    series = sonarr_client.get_series()

    episodes = sonarr_client.get_episode(series[0]["id"], True)
    assert isinstance(episodes, list)
    assert episodes[0]["id"]

    data = sonarr_client.get_episode(episodes[0]["id"])
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.get_episode(999)
        assert False


def test_upd_series(sonarr_client: SonarrAPI):
    series = sonarr_client.get_series()
    series[0]["monitored"] = False

    data = sonarr_client.upd_series(data=series[0], move_files=True)
    assert isinstance(data, dict)
    assert data["monitored"] is False


def test_get_episodes_by_series_id(sonarr_client: SonarrAPI):
    series = sonarr_client.get_series()
    data = sonarr_client.get_episodes_by_series_id(series[0]["id"])

    assert isinstance(data, list)

    with pytest.deprecated_call():
        sonarr_client.get_episodes_by_series_id(series[0]["id"])


def test_get_episode_by_episode_id(sonarr_client: SonarrAPI):
    series = sonarr_client.get_series()
    episodes = sonarr_client.get_episode(id_=series[0]["id"], series=True)
    data = sonarr_client.get_episode_by_episode_id(episodes[0]["id"])
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.get_episode_by_episode_id(999)
        assert False

    with pytest.deprecated_call():
        sonarr_client.get_episode_by_episode_id(episodes[0]["id"])


def test_get_episode_files_by_series_id(sonarr_client: SonarrAPI):
    series = sonarr_client.get_series()
    data = sonarr_client.get_episode_files_by_series_id(id_=series[0]["id"])
    assert isinstance(data, list)

    with pytest.deprecated_call():
        sonarr_client.get_episode_files_by_series_id(series[0]["id"])


def test_get_episode_file(sonarr_client: SonarrAPI):
    series = sonarr_client.get_series()
    episodes = sonarr_client.get_episode(id_=series[0]["id"], series=True)

    data = sonarr_client.get_episode_file(id_=series[0]["id"], series=True)
    assert isinstance(data, list)


def test_upd_episode(sonarr_client: SonarrAPI):
    series = sonarr_client.get_series()
    episodes = sonarr_client.get_episode(id_=series[0]["id"], series=True)

    payload = {"monitored": True}
    data = sonarr_client.upd_episode(episodes[0]["id"], payload)

    assert isinstance(data, dict)
    assert data["monitored"] == True


def test_upd_episode_monitor(sonarr_client: SonarrAPI):
    series = sonarr_client.get_series()
    episodes = sonarr_client.get_episode(id_=series[0]["id"], series=True)
    episode_ids = [d.get("id") for d in episodes]

    data = sonarr_client.upd_episode_monitor(episode_ids=episode_ids, monitored=False)

    assert isinstance(data, list)
    assert data[0]["monitored"] == False


def test_get_wanted(sonarr_client: SonarrAPI):
    data = sonarr_client.get_wanted()
    assert isinstance(data, dict)

    data = sonarr_client.get_wanted(include_series=True)
    assert isinstance(data, dict)

    data = sonarr_client.get_wanted(
        page=2,
        page_size=20,
        sort_key="series.sortTitle",
        sort_dir="ascending",
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_wanted(sort_key="timeleft")
        assert False

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_wanted(sort_dir="default")
        assert False


def test_get_history(sonarr_client: SonarrAPI):
    data = sonarr_client.get_history()
    assert isinstance(data, dict)

    series = sonarr_client.get_series()
    episodes = sonarr_client.get_episode(id_=series[0]["id"], series=True)
    data = sonarr_client.get_history()
    assert isinstance(data, dict)

    for key in ["id", "date", "eventType", "series.title", "episode.title"]:
        data = sonarr_client.get_history(
            page=1,
            page_size=10,
            sort_key=key,
            sort_dir="default",
            id_=episodes[0]["id"],
        )
        assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_history(sort_key="time")
        assert False

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_history(sort_dir="descending")
        assert False


def test_get_calendar(sonarr_client: SonarrAPI):
    start = datetime.strptime("Nov 30 2020  1:33PM", "%b %d %Y %I:%M%p")
    end = datetime.strptime("Dec 1 2020  1:33PM", "%b %d %Y %I:%M%p")
    data = sonarr_client.get_calendar(start_date=start, end_date=end)
    assert isinstance(data, list)

    start = datetime.strptime("Nov 30 2020  1:33PM", "%b %d %Y %I:%M%p")
    end = datetime.strptime("Dec 1 2020  1:33PM", "%b %d %Y %I:%M%p")
    data = sonarr_client.get_calendar(start_date=start, end_date=end, unmonitored=False)
    assert isinstance(data, list)


def test_get_indexer_schema(sonarr_client: SonarrAPI):
    data = sonarr_client.get_indexer_schema()
    assert isinstance(data, list)
    data = sonarr_client.get_indexer_schema(implementation="IPTorrents")
    assert isinstance(data, list)
    assert data[0]["implementation"] == "IPTorrents"

    with contextlib.suppress(PyarrRecordNotFound):
        data = sonarr_client.get_indexer_schema(implementation="polarbear")
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_get_indexer(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/indexer",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer_all.json"),
        status=200,
    )
    data = sonarr_mock_client.get_indexer()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer.json"),
        status=200,
    )
    data = sonarr_mock_client.get_indexer(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_upd_indexer(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer.json"),
        status=200,
    )
    data = sonarr_mock_client.get_indexer(1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer.json"),
        status=202,
    )
    data = sonarr_mock_client.upd_indexer(1, data)
    assert isinstance(data, dict)


def test_get_system_status(sonarr_client: SonarrAPI):
    data = sonarr_client.get_system_status()
    assert isinstance(data, dict)


def test_get_health(sonarr_client: SonarrAPI):
    data = sonarr_client.get_health()
    assert isinstance(data, list)


def test_get_metadata(sonarr_client: SonarrAPI):
    data = sonarr_client.get_metadata()
    assert isinstance(data, list)

    data = sonarr_client.get_metadata(data[0]["id"])
    assert isinstance(data, dict)


def test_get_update(sonarr_client: SonarrAPI):
    data = sonarr_client.get_update()
    assert isinstance(data, list)


def test_get_disk_space(sonarr_client: SonarrAPI):
    data = sonarr_client.get_disk_space()
    assert isinstance(data, list)


def test_get_backup(sonarr_client: SonarrAPI):
    data = sonarr_client.get_backup()
    assert isinstance(data, list)


def test_get_log(sonarr_client: SonarrAPI):
    data = sonarr_client.get_log()
    assert isinstance(data, dict)

    data = sonarr_client.get_log(
        page=10,
        page_size=10,
        sort_key="Id",
        sort_dir="descending",
        filter_key="level",
        filter_value="all",
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_log(sort_key="Id")
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_log(sort_dir="descending")
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_log(filter_key="level")
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_log(filter_value="all")
        assert False


def test_get_task(sonarr_client: SonarrAPI):
    data = sonarr_client.get_task()
    assert isinstance(data, list)

    data = sonarr_client.get_task(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_get_config_ui(sonarr_client: SonarrAPI):
    data = sonarr_client.get_config_ui()
    assert isinstance(data, dict)


def test_upd_config_ui(sonarr_client: SonarrAPI):
    payload = sonarr_client.get_config_ui()
    payload["enableColorImpairedMode"] = True
    data = sonarr_client.upd_config_ui(payload)
    assert isinstance(data, dict)
    assert data["enableColorImpairedMode"] == True


def test_get_config_host(sonarr_client: SonarrAPI):
    data = sonarr_client.get_config_host()
    assert isinstance(data, dict)


def test_upd_config_host(sonarr_client: SonarrAPI):
    payload = sonarr_client.get_config_host()
    payload["backupRetention"] = 29
    data = sonarr_client.upd_config_host(payload)

    assert isinstance(data, dict)
    assert data["backupRetention"] == 29


def test_get_config_naming(sonarr_client: SonarrAPI):
    data = sonarr_client.get_config_naming()
    assert isinstance(data, dict)


def test_upd_config_naming(sonarr_client: SonarrAPI):
    payload = sonarr_client.get_config_naming()
    payload["numberStyle"] = (
        "E{episode:00}S{season:00}"
        if payload["numberStyle"] == "S{season:00}E{episode:00}"
        else "S{season:00}E{episode:00}"
    )
    data = sonarr_client.upd_config_naming(payload)

    assert isinstance(data, dict)
    if payload["numberStyle"] == "S{season:00}E{episode:00}":
        assert data["numberStyle"] == "E{episode:00}S{season:00}"
    else:
        assert data["numberStyle"] == "S{season:00}E{episode:00}"


def test_get_media_management(sonarr_client: SonarrAPI):
    data = sonarr_client.get_media_management()
    assert isinstance(data, dict)


def test_upd_media_management(sonarr_client: SonarrAPI):
    payload = sonarr_client.get_media_management()
    payload["recycleBinCleanupDays"] = 6
    data = sonarr_client.upd_media_management(payload)

    assert isinstance(data, dict)
    assert data["recycleBinCleanupDays"] == 6


def test_get_notification_schema(sonarr_client: SonarrAPI):
    data = sonarr_client.get_notification_schema()
    assert isinstance(data, list)

    data = sonarr_client.get_notification_schema(implementation="Boxcar")
    assert isinstance(data, list)

    with contextlib.suppress(PyarrRecordNotFound):
        data = sonarr_client.get_notification_schema(implementation="polarbear")
        assert False


def test_create_tag(sonarr_client: SonarrAPI):
    data = sonarr_client.create_tag(label="string")
    assert isinstance(data, dict)


def test_get_tag(sonarr_client: SonarrAPI):
    data = sonarr_client.get_tag()
    assert isinstance(data, list)

    data = sonarr_client.get_tag(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_get_tag_detail(sonarr_client: SonarrAPI):
    data = sonarr_client.get_tag_detail()
    assert isinstance(data, list)

    data = sonarr_client.get_tag_detail(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_upd_tag(sonarr_client: SonarrAPI):
    tags = sonarr_client.get_tag()

    data = sonarr_client.upd_tag(id_=tags[0]["id"], label="newstring")
    assert isinstance(data, dict)
    assert data["label"] == "newstring"


def test_get_download_client_schema(sonarr_client: SonarrAPI):
    data = sonarr_client.get_download_client_schema()
    assert isinstance(data, list)

    data = sonarr_client.get_download_client_schema(implementation="Aria2")
    assert isinstance(data, list)

    with contextlib.suppress(PyarrRecordNotFound):
        data = sonarr_client.get_download_client_schema(implementation="polarbear")
        assert False


def test_get_import_list_schema(sonarr_client: SonarrAPI):
    data = sonarr_client.get_import_list_schema()
    assert isinstance(data, list)

    data = sonarr_client.get_import_list_schema(implementation="PlexImport")
    assert isinstance(data, list)

    with contextlib.suppress(PyarrRecordNotFound):
        data = sonarr_client.get_import_list_schema(implementation="polarbear")
        assert False


def test_get_releases(sonarr_client: SonarrAPI):
    data = sonarr_client.get_releases()
    assert isinstance(data, list)

    # TODO: Get release by ID, may require a mock


def test_get_quality_definition(sonarr_client: SonarrAPI):
    data = sonarr_client.get_quality_definition()
    assert isinstance(data, list)

    data = sonarr_client.get_quality_definition(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_upd_quality_definition(sonarr_client: SonarrAPI):
    rand_float = round(random.uniform(100.0, 199.9))

    quality_definitions = sonarr_client.get_quality_definition()
    quality_definition = sonarr_client.get_quality_definition(
        id_=quality_definitions[0]["id"]
    )
    quality_definition["maxSize"] = rand_float
    data = sonarr_client.upd_quality_definition(
        quality_definition["id"], quality_definition
    )
    assert isinstance(data, dict)
    assert data["maxSize"] == rand_float


def test_get_quality_profile_schema(sonarr_client: SonarrAPI):
    data = sonarr_client.get_quality_profile_schema()
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_get_queue(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/queue",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/queue.json"),
        status=200,
    )
    data = sonarr_mock_client.get_queue()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/queue",
        match=[
            matchers.query_string_matcher(
                "page=1&pageSize=20&sortKey=timeleft&sortDirection=default&includeUnknownSeriesItems=True&includeSeries=True&includeEpisode=True"
            )
        ],
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/queue.json"),
        status=200,
    )
    data = sonarr_mock_client.get_queue(
        page=1,
        page_size=20,
        sort_key="timeleft",
        sort_dir="default",
        include_unknown_series_items=True,
        include_series=True,
        include_episode=True,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_mock_client.get_queue(sort_key="timeleft")
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_mock_client.get_queue(sort_dir="default")
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_get_blocklist(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/blocklist",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blocklist.json"),
        status=200,
    )
    data = sonarr_mock_client.get_blocklist()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/blocklist",
        match=[
            matchers.query_string_matcher(
                "page=1&pageSize=10&sortKey=date&sortDirection=ascending"
            )
        ],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blocklist.json"),
        status=200,
    )
    data = sonarr_mock_client.get_blocklist(
        page=1,
        page_size=10,
        sort_key="date",
        sort_dir="ascending",
    )
    assert isinstance(data, dict)
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_mock_client.get_blocklist(sort_key="date")
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_mock_client.get_blocklist(sort_dir="ascending")
        assert False


def test_get_remote_path_mapping(sonarr_client: SonarrAPI):
    data = sonarr_client.get_remote_path_mapping()
    assert isinstance(data, list)


def test_get_notification(sonarr_client: SonarrAPI):
    data = sonarr_client.get_notification()
    assert isinstance(data, list)
    # TODO: Get notification by ID (required add_notification first)


def test_get_download_client(sonarr_client: SonarrAPI):
    data = sonarr_client.get_download_client()
    assert isinstance(data, list)
    # TODO: Get download client by ID (required add_download_client first)


def test_get_import_list(sonarr_client: SonarrAPI):
    data = sonarr_client.get_import_list()
    assert isinstance(data, list)


def test_get_config_download_client(sonarr_client: SonarrAPI):
    data = sonarr_client.get_config_download_client()
    assert isinstance(data, dict)


def test_upd_config_download_client(sonarr_client: SonarrAPI):
    dc_config = sonarr_client.get_config_download_client()
    dc_config["autoRedownloadFailed"] = False
    data = sonarr_client.upd_config_download_client(data=dc_config)
    assert isinstance(data, dict)
    assert data["autoRedownloadFailed"] == False


def test_get_parsed_title(sonarr_client: SonarrAPI):
    with pytest.deprecated_call():
        sonarr_client.get_parsed_title(title="test")


def test_post_command(sonarr_client: SonarrAPI):
    # RefreshSeries
    data = sonarr_client.post_command(name="RefreshSeries")
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    data = sonarr_client.post_command(
        "RefreshSeries", seriesId=sonarr_client.get_series()[0]["id"]
    )
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    # RescanSeries
    data = sonarr_client.post_command("RescanSeries")
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    data = sonarr_client.post_command(
        "RescanSeries", seriesId=sonarr_client.get_series()[0]["id"]
    )
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    # EpisodeSearch
    data = sonarr_client.post_command("EpisodeSearch", episodeIds=[1, 2, 3])
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    # SeasonSearch
    data = sonarr_client.post_command(
        "SeasonSearch", seriesId=sonarr_client.get_series()[0]["id"], seasonNumber=1
    )
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    # SeriesSearch
    data = sonarr_client.post_command(
        "SeriesSearch", seriesId=sonarr_client.get_series()[0]["id"]
    )
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    # DownloadedEpisodesScan
    data = sonarr_client.post_command(
        "DownloadedEpisodesScan", path=sonarr_client.get_root_folder()[0]["path"]
    )
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    # RSS Sync
    data = sonarr_client.post_command("RssSync")
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    # RenameFiles, NOTE: this test will always return a failed message on get_command
    # this would only work if we actually download files which we can't do on test.
    data = sonarr_client.post_command(
        "RenameFiles", seriesId=sonarr_client.get_series()[0]["id"], files=[1, 2, 3]
    )
    assert isinstance(data, dict)

    # RenameSeries
    data = sonarr_client.post_command(
        "RenameSeries", seriesIds=[sonarr_client.get_series()[0]["id"]]
    )
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    # Test backups
    data = sonarr_client.post_command("Backup")
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"

    data = sonarr_client.post_command("missingEpisodeSearch")
    time.sleep(5)
    result = sonarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "Completed"


def test_get_command(sonarr_client: SonarrAPI):
    """Check get_command()"""

    # No args
    data = sonarr_client.get_command()
    assert isinstance(data, list)

    # When an ID is supplied
    data = sonarr_client.get_command(data[0]["id"])
    assert isinstance(data, dict)

    # when an incorrect ID is supplied, not found response
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_client.get_command(4321)
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_get_parsed_path(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/parse",
        match=[matchers.query_string_matcher("path=/")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/parse.json"),
        status=200,
    )
    data = sonarr_mock_client.get_parsed_path("/")
    assert isinstance(data, dict)

    with pytest.deprecated_call():
        sonarr_mock_client.get_parsed_path(file_path="/")


@pytest.mark.usefixtures
@responses.activate
def test_post_release(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8989/api/v3/release",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/release_download.json"),
        status=201,
    )
    data = sonarr_mock_client.download_release(guid="1450590", indexer_id=2)
    assert isinstance(data, dict)


def test_get_parse_title_path(sonarr_client: SonarrAPI):
    data = sonarr_client.get_parse_title_path(title="test")
    assert isinstance(data, dict)

    data = sonarr_client.get_parse_title_path(path="/defaults")
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = sonarr_client.get_parse_title_path()
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_push_release(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8989/api/v3/release/push",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/release_download.json"),
        status=201,
    )
    data = sonarr_mock_client.push_release(
        title="test",
        download_url="https://ipt.beelyrics.net/t/1450590",
        protocol="Torrent",
        publish_date=datetime(2020, 5, 17),
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_upd_episode_file_quality(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/episodefile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episodefile.json"),
        status=202,
    )
    data = sonarr_mock_client.upd_episode_file_quality(
        1, load_fixture("sonarr/file_quality.json")
    )
    assert isinstance(data, dict)


# TODO: get correct fixture
@pytest.mark.usefixtures
@responses.activate
def test_get_manual_import(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/manualimport",
        match=[matchers.query_string_matcher("folder=/series/")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = sonarr_mock_client.get_manual_import(folder="/series/")
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/manualimport",
        match=[
            matchers.query_string_matcher(
                "folder=/series/&downloadId=1&seriesId=1&filterExistingFiles=True&replaceExistingFiles=True"
            )
        ],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = sonarr_mock_client.get_manual_import(
        folder="/series/",
        download_id=1,
        series_id=1,
        filter_existing_files=True,
        replace_existing_files=True,
    )
    assert isinstance(data, list)


# TODO: get correct fixture, confirm update returns dict
@pytest.mark.usefixtures
@responses.activate
def test_upd_manual_import(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/manualimport",
        match=[matchers.query_string_matcher("folder=/series/")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    man_import = sonarr_mock_client.get_manual_import(folder="/series/")

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/manualimport",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_dict.json"),
        status=200,
    )
    data = sonarr_mock_client.upd_manual_import(data=man_import)
    assert isinstance(data, dict)


# DELETE ACTIONS MUST BE LAST


def test_del_series(sonarr_client: SonarrAPI):
    series = sonarr_client.get_series()
    data = sonarr_client.del_series(series[0]["id"], delete_files=True)

    assert isinstance(data, dict)
    assert data == {}


def test_del_root_folder(sonarr_client: SonarrAPI):
    root_folders = sonarr_client.get_root_folder()

    # Check folder can be deleted
    data = sonarr_client.del_root_folder(root_folders[0]["id"])
    assert isinstance(data, dict)

    # Check that none existant root folder doesnt throw error
    data = sonarr_client.del_root_folder(999)
    assert isinstance(data, dict)


def test_del_tag(sonarr_client: SonarrAPI):
    tags = sonarr_client.get_tag()

    data = sonarr_client.del_tag(tags[0]["id"])
    assert isinstance(data, dict)
    assert data == {}


@pytest.mark.usefixtures
@responses.activate
def test_del_blocklist(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/blocklist/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = sonarr_mock_client.del_blocklist(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_blocklist_bulk(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/blocklist/bulk",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = sonarr_mock_client.del_blocklist_bulk(ids=[1, 2, 3])
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_indexer(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = sonarr_mock_client.del_indexer(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/indexer/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_mock_client.del_indexer(id_=999)
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_del_queue(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/queue/1",
        match=[matchers.query_string_matcher("removeFromClient=True&blocklist=True")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )

    data = sonarr_mock_client.del_queue(id_=1, remove_from_client=True, blocklist=True)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_episode_file(sonarr_mock_client: SonarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/episodefile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = sonarr_mock_client.del_episode_file(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/episodefile/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = sonarr_mock_client.del_episode_file(id_=999)
        assert False
