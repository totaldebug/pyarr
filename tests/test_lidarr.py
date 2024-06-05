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
from pyarr.lidarr import LidarrAPI

from tests import (
    LIDARR_ALBUM_TERM,
    LIDARR_ARTIST_TERM,
    LIDARR_MUSICBRAINZ_ALBUM_ID,
    LIDARR_MUSICBRAINZ_ARTIST_ID,
    LIDARR_TERM,
    load_fixture,
)


def test_add_root_folder(lidarr_client: LidarrAPI):
    qual_profile = lidarr_client.get_quality_profile()
    meta_profile = lidarr_client.get_metadata_profile()
    data = lidarr_client.add_root_folder(
        name="test",
        path="/defaults/",
        default_quality_profile_id=qual_profile[0]["id"],
        default_metadata_profile_id=meta_profile[0]["id"],
    )
    assert isinstance(data, dict)


def test_get_root_folder(lidarr_client: LidarrAPI):
    data = lidarr_client.get_root_folder()
    assert isinstance(data, list)

    data = lidarr_client.get_root_folder(data[0]["id"])
    assert isinstance(data, dict)


def test_lookup(lidarr_client: LidarrAPI):
    data = lidarr_client.lookup(term=LIDARR_TERM)
    assert isinstance(data, list)


def test_lookup_artist(lidarr_client: LidarrAPI):
    data = lidarr_client.lookup_artist(term=LIDARR_ARTIST_TERM)
    assert isinstance(data, list)


def test_lookup_album(lidarr_client: LidarrAPI):
    data = lidarr_client.lookup_album(term=LIDARR_ALBUM_TERM)
    assert isinstance(data, list)


def test_add_artist(lidarr_client: LidarrAPI):
    qual_profile = lidarr_client.get_quality_profile()
    meta_profile = lidarr_client.get_metadata_profile()
    items = lidarr_client.lookup(term=f"lidarr:{LIDARR_MUSICBRAINZ_ARTIST_ID}")

    for item in items:
        if "artist" in item:
            artist = item["artist"]
            data = lidarr_client.add_artist(
                artist=artist,
                root_dir="/",
                quality_profile_id=qual_profile[0]["id"],
                metadata_profile_id=meta_profile[0]["id"],
                monitored=False,
                artist_monitor="latest",
                artist_search_for_missing_albums=False,
            )
            break
        if item == items[-1]:
            assert False
    assert isinstance(data, dict)


def test_get_artist(lidarr_client: LidarrAPI):
    data = lidarr_client.get_artist()
    assert isinstance(data, list)

    data = lidarr_client.get_artist(id_=data[0]["id"])
    assert isinstance(data, dict)

    data = lidarr_client.get_artist(id_=LIDARR_MUSICBRAINZ_ARTIST_ID)
    assert isinstance(data, list)


def test_upd_artist(lidarr_client: LidarrAPI):
    artist = lidarr_client.get_artist()

    data = lidarr_client.upd_artist(data=artist[0])
    assert isinstance(data, dict)


def test_add_album(lidarr_client: LidarrAPI):
    qual_profile = lidarr_client.get_quality_profile()
    meta_profile = lidarr_client.get_metadata_profile()
    items = lidarr_client.lookup(f"lidarr:{LIDARR_MUSICBRAINZ_ALBUM_ID}")

    for item in items:
        if "album" in item:
            album = item["album"]
            data = lidarr_client.add_album(
                album=album,
                root_dir="/defaults/",
                quality_profile_id=qual_profile[0]["id"],
                metadata_profile_id=meta_profile[0]["id"],
                monitored=False,
                artist_monitor="latest",
                artist_search_for_missing_albums=False,
            )
            break
        if item == items[-1]:
            assert False

    assert isinstance(data, dict)

    items = lidarr_client.lookup(LIDARR_ALBUM_TERM)

    for item in items:
        if "album" in item:
            album = item["album"]
            data = lidarr_client.add_album(
                album=album,
                root_dir="/defaults/",
                quality_profile_id=qual_profile[0]["id"],
                metadata_profile_id=meta_profile[0]["id"],
                monitored=False,
                artist_monitor="latest",
                artist_search_for_missing_albums=False,
            )
            break
        if item == items[-1]:
            assert False

    assert isinstance(data, dict)


def test_upd_album(lidarr_client: LidarrAPI):
    album = lidarr_client.get_album()

    data = lidarr_client.upd_album(data=album[0])
    assert isinstance(data, dict)


def test_get_album(lidarr_client: LidarrAPI):
    data = lidarr_client.get_album()
    assert isinstance(data, list)

    data = lidarr_client.get_album(artistId=data[0]["artistId"], allArtistAlbums=True)
    assert isinstance(data, list)

    data = lidarr_client.get_album(foreignAlbumId=LIDARR_MUSICBRAINZ_ARTIST_ID)
    assert isinstance(data, list)


def test_get_wanted(lidarr_client: LidarrAPI):
    data = lidarr_client.get_wanted()
    assert isinstance(data, dict)

    data = lidarr_client.get_wanted(missing=False)
    assert isinstance(data, dict)

    data = lidarr_client.get_wanted(
        page=1,
        page_size=20,
        sort_key="albums.title",
        sort_dir="ascending",
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_wanted(sort_key="timeleft")
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_wanted(sort_dir="default")
        assert False


# TODO: confirm fixture
@pytest.mark.usefixtures
@responses.activate
def test_get_parse(lidarr_mock_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/parse",
        match=[matchers.query_string_matcher("title=test")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_parse(title="test")
    assert isinstance(data, list)


def test_get_tracks(lidarr_client: LidarrAPI):
    artist = lidarr_client.get_artist()
    album = lidarr_client.get_album()

    data = lidarr_client.get_tracks(artistId=artist[0]["id"])
    assert isinstance(data, list)

    data = lidarr_client.get_tracks(albumId=album[0]["id"])
    assert isinstance(data, list)

    data = lidarr_client.get_tracks(albumReleaseId=album[0]["releases"][0]["id"])
    assert isinstance(data, list)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_tracks()
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_get_track_file(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile",
        match=[matchers.query_string_matcher("artistId=1")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
    )
    data = lidarr_mock_client.get_track_file(artistId=1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile",
        match=[matchers.query_string_matcher("albumId=1")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
    )
    data = lidarr_mock_client.get_track_file(albumId=1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile",
        match=[
            matchers.query_string_matcher(
                "trackFileIds=1&trackFileIds=2&trackFileIds=3"
            )
        ],
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
    )
    data = lidarr_mock_client.get_track_file(trackFileIds=[1, 2, 3])
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track.json"),
        status=200,
    )
    data = lidarr_mock_client.get_track_file(trackFileIds=1)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile",
        match=[matchers.query_string_matcher("unmapped=True")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
    )
    data = lidarr_mock_client.get_track_file(unmapped=True)
    assert isinstance(data, list)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_mock_client.get_track_file()
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_upd_track_file(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track.json"),
        status=200,
    )
    track = lidarr_mock_client.get_track_file(trackFileIds=1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/trackfile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track.json"),
        status=200,
    )
    data = lidarr_mock_client.upd_track_file(data=track)
    assert isinstance(data, dict)


def test_get_metadata_profile(lidarr_client: LidarrAPI):
    data = lidarr_client.get_metadata_profile()
    assert isinstance(data, list)

    data = lidarr_client.get_metadata_profile(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_upd_metadata_profile(lidarr_client: LidarrAPI):
    profile = lidarr_client.get_metadata_profile()

    data = lidarr_client.upd_metadata_profile(data=profile[0])
    assert isinstance(data, dict)


def test_get_metadata_provider(lidarr_client: LidarrAPI):
    data = lidarr_client.get_metadata_provider()
    assert isinstance(data, dict)


def test_upd_metadata_provider(lidarr_client: LidarrAPI):
    provider = lidarr_client.get_metadata_provider()

    data = lidarr_client.upd_metadata_provider(data=provider)
    assert isinstance(data, dict)


def test_get_language(lidarr_client: LidarrAPI):
    data = lidarr_client.get_language()
    assert isinstance(data, list)

    data = lidarr_client.get_language(data[0]["id"])
    assert isinstance(data, dict)


def test_post_command(lidarr_client: LidarrAPI):
    data = lidarr_client.post_command(
        name="DownloadedAlbumsScan", path=lidarr_client.get_root_folder()[0]["path"]
    )
    time.sleep(5)
    result = lidarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["status"] == "completed"

    data = lidarr_client.post_command(
        name="ArtistSearch", artistId=lidarr_client.get_artist()[0]["id"]
    )
    time.sleep(5)
    result = lidarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["status"] == "completed"

    data = lidarr_client.post_command(name="RefreshArtist")
    time.sleep(5)
    result = lidarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["status"] == "completed"

    data = lidarr_client.post_command(name="RefreshAlbum")
    time.sleep(5)
    result = lidarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["status"] == "completed"

    data = lidarr_client.post_command(name="ApplicationUpdateCheck")
    time.sleep(5)
    result = lidarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["message"] == "No update available"

    data = lidarr_client.post_command(name="MissingAlbumSearch")
    time.sleep(5)
    result = lidarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["status"] == "completed"

    data = lidarr_client.post_command(name="AlbumSearch")
    assert isinstance(data, dict)

    data = lidarr_client.post_command(name="RssSync")
    time.sleep(5)
    result = lidarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["status"] == "completed"

    data = lidarr_client.post_command(name="Backup")
    time.sleep(5)
    result = lidarr_client.get_command(id_=data["id"])
    assert isinstance(data, dict)
    assert result["status"] == "completed"


@pytest.mark.usefixtures
@responses.activate
def test_get_queue(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/queue.json"),
        status=200,
    )
    data = lidarr_mock_client.get_queue()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue",
        match=[
            matchers.query_string_matcher(
                "page=1&pageSize=10&sortKey=timeleft&sortDirection=default"
            )
        ],
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/queue.json"),
        status=200,
    )
    data = lidarr_mock_client.get_queue(
        page=1,
        page_size=10,
        sort_key="timeleft",
        sort_dir="default",
    )
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue",
        match=[
            matchers.query_string_matcher(
                "unknownArtists=True&includeAlbum=True&includeArtist=True"
            )
        ],
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/queue.json"),
        status=200,
    )
    data = lidarr_mock_client.get_queue(
        unknown_artists=True, include_album=True, include_artist=True
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_mock_client.get_queue(sort_key="artistId")
        assert False

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_mock_client.get_queue(sort_dir="ascending")
        assert False


# TODO: get correct fixture
@pytest.mark.usefixtures
@responses.activate
def test_get_queue_details(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue/details",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_queue_details()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue/details",
        match=[
            matchers.query_string_matcher(
                "includeArtist=True&includeAlbum=True&artistId=1&albumIds=1&albumIds=2"
            )
        ],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_queue_details(
        include_artist=True, include_album=True, artistId=1, albumIds=[1, 2]
    )
    assert isinstance(data, list)


# TODO: get correct fixture
@pytest.mark.usefixtures
@responses.activate
def test_get_release(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/release",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_release()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/release",
        match=[matchers.query_string_matcher("artistId=1&albumId=1")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_release(artistId=1, albumId=1)
    assert isinstance(data, list)


# TODO: get correct fixture
@pytest.mark.usefixtures
@responses.activate
def test_get_rename(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/rename",
        match=[matchers.query_string_matcher("artistId=1")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_rename(artistId=1)
    assert isinstance(data, list)
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/rename",
        match=[matchers.query_string_matcher("artistId=1&albumId=1")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_rename(artistId=1, albumId=1)
    assert isinstance(data, list)

    with contextlib.suppress(TypeError):
        data = lidarr_mock_client.get_rename()
        assert False


# TODO: get correct fixture
@pytest.mark.usefixtures
@responses.activate
def test_get_manual_import(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/manualimport",
        match=[matchers.query_string_matcher("folder=/music/")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_manual_import(folder="/music/")
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/manualimport",
        match=[
            matchers.query_string_matcher(
                "folder=/music/&downloadId=1&artistId=1&filterExistingFiles=True&replaceExistingFiles=True"
            )
        ],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_manual_import(
        folder="/music/",
        downloadId=1,
        artistId=1,
        filterExistingFiles=True,
        replaceExistingFiles=True,
    )
    assert isinstance(data, list)


# TODO: get correct fixture, confirm update returns dict
@pytest.mark.usefixtures
@responses.activate
def test_upd_manual_import(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/manualimport",
        match=[matchers.query_string_matcher("folder=/music/")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    man_import = lidarr_mock_client.get_manual_import(folder="/music/")

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/manualimport",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_dict.json"),
        status=200,
    )
    data = lidarr_mock_client.upd_manual_import(data=man_import)
    assert isinstance(data, dict)


# TODO: get correct fixture
@pytest.mark.usefixtures
@responses.activate
def test_get_retag(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/retag",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_retag()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/retag",
        match=[matchers.query_string_matcher("artistId=1&albumId=1")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
    )
    data = lidarr_mock_client.get_retag(artistId=1, albumId=1)
    assert isinstance(data, list)


def test_get_calendar(lidarr_client: LidarrAPI):
    start = datetime.strptime("Nov 30 2020  1:33PM", "%b %d %Y %I:%M%p")
    end = datetime.strptime("Dec 1 2020  1:33PM", "%b %d %Y %I:%M%p")
    data = lidarr_client.get_calendar(start_date=start, end_date=end)
    assert isinstance(data, list)

    start = datetime.strptime("Nov 30 2020  1:33PM", "%b %d %Y %I:%M%p")
    end = datetime.strptime("Dec 1 2020  1:33PM", "%b %d %Y %I:%M%p")
    data = lidarr_client.get_calendar(start_date=start, end_date=end, unmonitored=False)
    assert isinstance(data, list)


def test_get_system_status(lidarr_client: LidarrAPI):
    data = lidarr_client.get_system_status()
    assert isinstance(data, dict)


def test_get_health(lidarr_client: LidarrAPI):
    data = lidarr_client.get_health()
    assert isinstance(data, list)


def test_get_metadata(lidarr_client: LidarrAPI):
    data = lidarr_client.get_metadata()
    assert isinstance(data, list)

    data = lidarr_client.get_metadata(data[0]["id"])
    assert isinstance(data, dict)


def test_get_update(lidarr_client: LidarrAPI):
    data = lidarr_client.get_update()
    assert isinstance(data, list)


def test_get_disk_space(lidarr_client: LidarrAPI):
    data = lidarr_client.get_disk_space()
    assert isinstance(data, list)


def test_get_backup(lidarr_client: LidarrAPI):
    data = lidarr_client.get_backup()
    assert isinstance(data, list)


def test_get_log(lidarr_client: LidarrAPI):
    data = lidarr_client.get_log()
    assert isinstance(data, dict)

    data = lidarr_client.get_log(
        page=10,
        page_size=10,
        sort_key="Id",
        sort_dir="descending",
        filter_key="level",
        filter_value="all",
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_log(sort_key="Id")
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_log(sort_dir="descending")
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_log(filter_key="level")
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_log(filter_value="all")
        assert False


def test_get_task(lidarr_client: LidarrAPI):
    data = lidarr_client.get_task()
    assert isinstance(data, list)

    data = lidarr_client.get_task(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_get_config_ui(lidarr_client: LidarrAPI):
    data = lidarr_client.get_config_ui()
    assert isinstance(data, dict)


def test_upd_config_ui(lidarr_client: LidarrAPI):
    payload = lidarr_client.get_config_ui()
    payload["enableColorImpairedMode"] = True
    data = lidarr_client.upd_config_ui(payload)
    assert isinstance(data, dict)
    assert data["enableColorImpairedMode"] == True


def test_get_config_host(lidarr_client: LidarrAPI):
    data = lidarr_client.get_config_host()
    assert isinstance(data, dict)


def test_upd_config_host(lidarr_client: LidarrAPI):
    payload = lidarr_client.get_config_host()
    payload["backupRetention"] = 29
    data = lidarr_client.upd_config_host(payload)

    assert isinstance(data, dict)
    assert data["backupRetention"] == 29


def test_get_config_naming(lidarr_client: LidarrAPI):
    data = lidarr_client.get_config_naming()
    assert isinstance(data, dict)


def test_upd_config_naming(lidarr_client: LidarrAPI):
    payload = lidarr_client.get_config_naming()
    payload["standardTrackFormat"] = (
        "{Album Title} - {track:00} - {Track Title} - {Album Title} ({Release Year})/{Artist Name}"
        if payload["standardTrackFormat"]
        == "{Album Title} ({Release Year})/{Artist Name} - {Album Title} - {track:00} - {Track Title}"
        else "{Album Title} ({Release Year})/{Artist Name} - {Album Title} - {track:00} - {Track Title}"
    )
    data = lidarr_client.upd_config_naming(payload)

    assert isinstance(data, dict)


def test_get_media_management(lidarr_client: LidarrAPI):
    data = lidarr_client.get_media_management()
    assert isinstance(data, dict)


def test_upd_media_management(lidarr_client: LidarrAPI):
    payload = lidarr_client.get_media_management()
    payload["recycleBinCleanupDays"] = 6
    data = lidarr_client.upd_media_management(payload)

    assert isinstance(data, dict)
    assert data["recycleBinCleanupDays"] == 6


def test_get_notification_schema(lidarr_client: LidarrAPI):
    data = lidarr_client.get_notification_schema()
    assert isinstance(data, list)

    data = lidarr_client.get_notification_schema(implementation="Apprise")
    assert isinstance(data, list)

    with contextlib.suppress(PyarrRecordNotFound):
        data = lidarr_client.get_notification_schema(implementation="polarbear")
        assert False


def test_create_tag(lidarr_client: LidarrAPI):
    data = lidarr_client.create_tag(label="string")
    assert isinstance(data, dict)


def test_get_tag(lidarr_client: LidarrAPI):
    data = lidarr_client.get_tag()
    assert isinstance(data, list)

    data = lidarr_client.get_tag(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_get_tag_detail(lidarr_client: LidarrAPI):
    data = lidarr_client.get_tag_detail()
    assert isinstance(data, list)

    data = lidarr_client.get_tag_detail(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_upd_tag(lidarr_client: LidarrAPI):
    tags = lidarr_client.get_tag()

    data = lidarr_client.upd_tag(id_=tags[0]["id"], label="newstring")
    assert isinstance(data, dict)
    assert data["label"] == "newstring"


def test_get_history(lidarr_client: LidarrAPI):
    data = lidarr_client.get_history()
    assert isinstance(data, dict)

    for key in ["id", "date", "eventType", "sourceTitle"]:
        data = lidarr_client.get_history(
            page=1,
            page_size=10,
            sort_key=key,
            sort_dir="default",
        )
        assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_history(sort_key="date")
        assert False

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_history(sort_dir="descending")
        assert False


def test_add_quality_profile(lidarr_client: LidarrAPI):
    language = lidarr_client.get_language()[0]
    schema = lidarr_client.get_quality_profile_schema()
    schema["items"][1]["allowed"] = True

    data = lidarr_client.add_quality_profile(
        name="music",
        upgrade_allowed=True,
        cutoff=schema["items"][1]["id"],
        schema=schema,
        language=language,
    )
    assert isinstance(data, dict)


def test_upd_quality_profile(lidarr_client: LidarrAPI):
    quality_profiles = lidarr_client.get_quality_profile()

    data = lidarr_client.upd_quality_profile(
        id_=quality_profiles[0]["id"], data=quality_profiles[0]
    )
    assert isinstance(data, dict)


def test_get_quality_definition(lidarr_client: LidarrAPI):
    data = lidarr_client.get_quality_definition()
    assert isinstance(data, list)

    data = lidarr_client.get_quality_definition(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_upd_quality_definition(lidarr_client: LidarrAPI):
    rand_float = round(random.uniform(100.0, 199.9))

    quality_definitions = lidarr_client.get_quality_definition()
    quality_definition = lidarr_client.get_quality_definition(
        id_=quality_definitions[0]["id"]
    )
    quality_definition["maxSize"] = rand_float
    data = lidarr_client.upd_quality_definition(
        quality_definition["id"], quality_definition
    )
    assert isinstance(data, dict)
    assert data["maxSize"] == rand_float


def test_get_quality_profile_schema(lidarr_client: LidarrAPI):
    data = lidarr_client.get_quality_profile_schema()
    assert isinstance(data, dict)


def test_get_indexer_schema(lidarr_client: LidarrAPI):
    data = lidarr_client.get_indexer_schema()
    assert isinstance(data, list)
    data = lidarr_client.get_indexer_schema(implementation="IPTorrents")
    assert isinstance(data, list)
    assert data[0]["implementation"] == "IPTorrents"

    with contextlib.suppress(PyarrRecordNotFound):
        data = lidarr_client.get_indexer_schema(implementation="polarbear")
        assert False


def test_get_remote_path_mapping(lidarr_client: LidarrAPI):
    data = lidarr_client.get_remote_path_mapping()
    assert isinstance(data, list)


def test_get_notification(lidarr_client: LidarrAPI):
    data = lidarr_client.get_notification()
    assert isinstance(data, list)
    # TODO: Get notification by ID (required add_notification first)


def test_get_download_client(lidarr_client: LidarrAPI):
    data = lidarr_client.get_download_client()
    assert isinstance(data, list)
    # TODO: Get download client by ID (required add_download_client first)


def test_get_import_list(lidarr_client: LidarrAPI):
    data = lidarr_client.get_import_list()
    assert isinstance(data, list)


def test_get_config_download_client(lidarr_client: LidarrAPI):
    data = lidarr_client.get_config_download_client()
    assert isinstance(data, dict)


def test_upd_config_download_client(lidarr_client: LidarrAPI):
    dc_config = lidarr_client.get_config_download_client()
    dc_config["autoRedownloadFailed"] = False
    data = lidarr_client.upd_config_download_client(data=dc_config)
    assert isinstance(data, dict)
    assert data["autoRedownloadFailed"] == False


def test_get_download_client_schema(lidarr_client: LidarrAPI):
    data = lidarr_client.get_download_client_schema()
    assert isinstance(data, list)

    data = lidarr_client.get_download_client_schema(implementation="Aria2")
    assert isinstance(data, list)

    with contextlib.suppress(PyarrRecordNotFound):
        data = lidarr_client.get_download_client_schema(implementation="polarbear")
        assert False


def test_get_import_list_schema(lidarr_client: LidarrAPI):
    data = lidarr_client.get_import_list_schema()
    assert isinstance(data, list)

    data = lidarr_client.get_import_list_schema(implementation="HeadphonesImport")
    assert isinstance(data, list)

    with contextlib.suppress(PyarrRecordNotFound):
        data = lidarr_client.get_import_list_schema(implementation="polarbear")
        assert False


def test_get_command(lidarr_client: LidarrAPI):
    """Check get_command()"""

    # No args
    data = lidarr_client.get_command()
    assert isinstance(data, list)

    # When an ID is supplied
    data = lidarr_client.get_command(data[0]["id"])
    assert isinstance(data, dict)

    # when an incorrect ID is supplied, not found response
    with contextlib.suppress(PyarrResourceNotFound):
        data = lidarr_client.get_command(4321)
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_get_indexer(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/indexer",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer_all.json"),
        status=200,
    )
    data = lidarr_mock_client.get_indexer()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer.json"),
        status=200,
    )
    data = lidarr_mock_client.get_indexer(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_upd_indexer(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer.json"),
        status=200,
    )
    data = lidarr_mock_client.get_indexer(1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer.json"),
        status=202,
    )
    data = lidarr_mock_client.upd_indexer(1, data)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_get_blocklist(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/blocklist",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blocklist.json"),
        status=200,
    )
    data = lidarr_mock_client.get_blocklist()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/blocklist",
        match=[
            matchers.query_string_matcher(
                "page=1&pageSize=10&sortKey=date&sortDirection=ascending"
            )
        ],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blocklist.json"),
        status=200,
    )
    data = lidarr_mock_client.get_blocklist(
        page=1,
        page_size=10,
        sort_key="date",
        sort_dir="ascending",
    )
    assert isinstance(data, dict)
    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_mock_client.get_blocklist(sort_key="date")
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_mock_client.get_blocklist(sort_dir="ascending")
        assert False


### DELETE BELOW HERE


def test_delete_album(lidarr_client: LidarrAPI):
    album = lidarr_client.get_album()
    data = lidarr_client.delete_album(album[0]["id"])
    assert data.status_code == 200


def test_delete_artist(lidarr_client: LidarrAPI):
    artist = lidarr_client.get_artist()
    data = lidarr_client.delete_artist(artist[0]["id"])
    assert data.status_code == 200


def test_del_root_folder(lidarr_client: LidarrAPI):
    root_folders = lidarr_client.get_root_folder()

    # Check folder can be deleted
    data = lidarr_client.del_root_folder(root_folders[0]["id"])
    assert data.status_code == 200

    # Check that none existant root folder doesnt throw error
    with contextlib.suppress(PyarrResourceNotFound):
        data = lidarr_client.del_root_folder(999)
        assert False


def test_del_quality_profile(lidarr_client: LidarrAPI):
    quality_profiles = lidarr_client.get_quality_profile()

    for profile in quality_profiles:
        if profile["name"] == "music":
            # Check folder can be deleted
            data = lidarr_client.del_quality_profile(profile["id"])
            assert data.status_code == 200

    # Check that none existant doesnt throw error
    data = lidarr_client.del_quality_profile(999)
    assert data.status_code == 200


def test_del_tag(lidarr_client: LidarrAPI):
    tags = lidarr_client.get_tag()

    data = lidarr_client.del_tag(tags[0]["id"])
    assert data.status_code == 200


@pytest.mark.usefixtures
@responses.activate
def test_delete_track_file(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/trackfile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = lidarr_mock_client.delete_track_file(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_blocklist(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/blocklist/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = lidarr_mock_client.del_blocklist(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_blocklist_bulk(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/blocklist/bulk",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = lidarr_mock_client.del_blocklist_bulk(ids=[1, 2, 3])
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_indexer(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = lidarr_mock_client.del_indexer(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/indexer/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = lidarr_mock_client.del_indexer(id_=999)
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_del_queue(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/queue/1",
        match=[matchers.query_string_matcher("removeFromClient=True&blocklist=True")],
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )

    data = lidarr_mock_client.del_queue(id_=1, remove_from_client=True, blocklist=True)
    assert isinstance(data, dict)
