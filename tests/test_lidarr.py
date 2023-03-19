import contextlib

import pytest
import responses

from pyarr.exceptions import (
    PyarrMissingArgument,
    PyarrMissingProfile,
    PyarrRecordNotFound,
    PyarrResourceNotFound,
)
from pyarr.lidarr import LidarrAPI
from pyarr.models.common import PyarrSortDirection
from pyarr.models.lidarr import LidarrArtistMonitor, LidarrCommand, LidarrSortKey

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
        qualityProfile=qual_profile[0]["id"],
        metadataProfile=meta_profile[0]["id"],
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


def test__artist_json(lidarr_client: LidarrAPI):
    qual_profile = lidarr_client.get_quality_profile()
    meta_profile = lidarr_client.get_metadata_profile()

    data = lidarr_client._artist_json(
        id_=LIDARR_MUSICBRAINZ_ARTIST_ID,
        root_dir="/",
        quality_profile_id=qual_profile[0]["id"],
        metadata_profile_id=meta_profile[0]["id"],
        monitored=False,
        artist_monitor=LidarrArtistMonitor.FIRST_ALBUM,
        artist_search_for_missing_albums=False,
    )
    assert isinstance(data, dict)


def test_add_artist(lidarr_client: LidarrAPI):
    qual_profile = lidarr_client.get_quality_profile()
    meta_profile = lidarr_client.get_metadata_profile()

    data = lidarr_client.add_artist(
        id_=LIDARR_MUSICBRAINZ_ARTIST_ID,
        root_dir="/",
        quality_profile_id=qual_profile[0]["id"],
        metadata_profile_id=meta_profile[0]["id"],
        monitored=False,
        artist_monitor=LidarrArtistMonitor.LATEST_ALBUM,
        artist_search_for_missing_albums=False,
    )
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

    data = lidarr_client.upd_artist(data=artist)
    assert isinstance(data, dict)


def test__album_json(lidarr_client: LidarrAPI):
    qual_profile = lidarr_client.get_quality_profile()
    meta_profile = lidarr_client.get_metadata_profile()

    data = lidarr_client._album_json(
        id_=LIDARR_MUSICBRAINZ_ALBUM_ID,
        root_dir="/",
        quality_profile_id=qual_profile[0]["id"],
        metadata_profile_id=meta_profile[0]["id"],
        monitored=False,
        artist_monitor=LidarrArtistMonitor.FIRST_ALBUM,
        artist_search_for_missing_albums=False,
    )
    assert isinstance(data, dict)


def test_add_album(lidarr_client: LidarrAPI):

    qual_profile = lidarr_client.get_quality_profile()
    meta_profile = lidarr_client.get_metadata_profile()

    data = lidarr_client.add_album(
        id_=LIDARR_MUSICBRAINZ_ALBUM_ID,
        root_dir="/defaults/",
        quality_profile_id=qual_profile[0]["id"],
        metadata_profile_id=meta_profile[0]["id"],
        monitored=False,
        artist_monitor=LidarrArtistMonitor.LATEST_ALBUM,
        artist_search_for_missing_albums=False,
    )
    assert isinstance(data, dict)


def test_upd_album(lidarr_client: LidarrAPI):

    album = lidarr_client.get_album()

    data = lidarr_client.upd_album(data=album[0]["id"])
    assert isinstance(data, dict)


def test_get_album(lidarr_client: LidarrAPI):

    data = lidarr_client.get_album()
    assert isinstance(data, list)

    data = lidarr_client.get_album(albumIds=data[0]["id"])
    assert isinstance(data, dict)

    data = lidarr_client.get_album(artistId=data[0]["artistId"], allArtistAlbums=True)
    assert isinstance(data, list)

    data = lidarr_client.get_album(foreignAlbumId=LIDARR_MUSICBRAINZ_ARTIST_ID)
    assert isinstance(data, dict)


def test_post_command(lidarr_client: LidarrAPI):

    data = lidarr_client.post_command(name=LidarrCommand.DOWNLOADED_ALBUMS_SCAN)
    assert isinstance(data, dict)
    data = lidarr_client.post_command(name=LidarrCommand.ARTIST_SEARCH)
    assert isinstance(data, dict)
    data = lidarr_client.post_command(name=LidarrCommand.REFRESH_ARTIST)
    assert isinstance(data, dict)
    data = lidarr_client.post_command(name=LidarrCommand.REFRESH_ALBUM)
    assert isinstance(data, dict)
    data = lidarr_client.post_command(name=LidarrCommand.APP_UPDATE_CHECK)
    assert isinstance(data, dict)
    data = lidarr_client.post_command(name=LidarrCommand.MISSING_ALBUM_SEARCH)
    assert isinstance(data, dict)
    data = lidarr_client.post_command(name=LidarrCommand.ALBUM_SEARCH)
    assert isinstance(data, dict)


def test_get_wanted(lidarr_client: LidarrAPI):

    data = lidarr_client.get_wanted()
    assert isinstance(data, dict)

    data = lidarr_client.get_wanted(missing=False)
    assert isinstance(data, dict)

    data = lidarr_client.get_wanted(
        page=1,
        page_size=20,
        sort_key=LidarrSortKey.ALBUM_TITLE,
        sort_dir=PyarrSortDirection.ASC,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_wanted(sort_key=LidarrSortKey.TIMELEFT)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_wanted(sort_dir=PyarrSortDirection.DEFAULT)
        assert False


# TODO: confirm fixture
@pytest.mark.usefixtures
@responses.activate
def test_get_parse(lidarr_mock_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/parse?title=test",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
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

    data = lidarr_client.get_tracks(albumReleaseId=1)
    assert isinstance(data, list)

    data = lidarr_client.get_tracks(trackIds=1)
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_tracks()
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_get_track_file(lidarr_mock_client: LidarrAPI):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile?artistId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_track_file(artistId=1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile?albumId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_track_file(albumId=1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile?trackFileIds=1&trackFileIds=2&trackFileIds=3",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_track_file(trackFileIds=[1, 2, 3])
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_track_file(trackFileIds=1)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile?unmapped=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
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
        match_querystring=True,
    )
    track = lidarr_mock_client.get_track_file(trackFileIds=1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/trackfile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track.json"),
        status=200,
        match_querystring=True,
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


@pytest.mark.usefixtures
@responses.activate
def test_get_queue(lidarr_mock_client: LidarrAPI):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_queue()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue?page=1&pageSize=10&sortKey=timeleft&sortDirection=default",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_queue(
        page=1,
        page_size=10,
        sort_key=LidarrSortKey.TIMELEFT,
        sort_dir=PyarrSortDirection.DEFAULT,
    )
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue?unknownArtists=True&includeAlbum=True&includeArtist=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_queue(
        unknown_artists=True, include_album=True, include_artist=True
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_mock_client.get_queue(sort_key=LidarrSortKey.ARTIST_ID)
        assert False

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_mock_client.get_queue(sort_dir=PyarrSortDirection.ASC)
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
        match_querystring=True,
    )
    data = lidarr_mock_client.get_queue_details()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue/details?includeArtist=True&includeAlbum=True&artistId=1&albumIds=1&albumIds=2",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
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
        match_querystring=True,
    )
    data = lidarr_mock_client.get_release()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/release?artistId=1&albumId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_release(artistId=1, albumId=1)
    assert isinstance(data, list)


# TODO: get correct fixture
@pytest.mark.usefixtures
@responses.activate
def test_get_rename(lidarr_mock_client: LidarrAPI):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/rename?artistId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_rename(artistId=1)
    assert isinstance(data, list)
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/rename?artistId=1&albumId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
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
        "https://127.0.0.1:8686/api/v1/manualimport?folder=/music/",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_manual_import(folder="/music/")
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/manualimport?folder=/music/&downloadId=1&artistId=1&filterExistingFiles=True&replaceExistingFiles=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
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
        "https://127.0.0.1:8686/api/v1/manualimport?folder=/music/",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    man_import = lidarr_mock_client.get_manual_import(folder="/music/")

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/manualimport",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_dict.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.upd_manual_import(data=man_import)
    assert isinstance(data, dict)


# TODO: get correct fixture
@pytest.mark.usefixtures
@responses.activate
def test_get_manual_import(lidarr_mock_client: LidarrAPI):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/retag",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_retag()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/retag?artistId=1&albumId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.get_retag(artistId=1, albumId=1)
    assert isinstance(data, list)


def test_delete_album(lidarr_client: LidarrAPI):
    album = lidarr_client.get_album()
    data = lidarr_client.delete_album(album[0]["id"])
    assert isinstance(data, dict)


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


@pytest.mark.usefixtures
@responses.activate
def test_delete_track_file(lidarr_mock_client: LidarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/trackfile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_mock_client.delete_track_file(1)
    assert isinstance(data, dict)
