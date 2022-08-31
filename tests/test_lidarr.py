import contextlib

import pytest

from pyarr.exceptions import PyarrMissingArgument, PyarrMissingProfile
from pyarr.models.common import PyarrSortDirection
from pyarr.models.lidarr import LidarrArtistMonitor, LidarrCommand, LidarrSortKey

from tests import load_fixture


@pytest.mark.usefixtures
def test_add_root_folder(responses, lidarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8686/api/v1/rootfolder",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/rootfolder.json"),
        status=201,
        match_querystring=True,
    )
    data = lidarr_client.add_root_folder(
        name="test", path="/path/to/folder", qualityProfile=1, metadataProfile=1
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_lookup(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/search?term=my+string",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.lookup(term="my string")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_lookup_artist(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist/lookup?term=my+string",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.lookup_artist(term="my string")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_lookup_album(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/album/lookup?term=my+string",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.lookup_album(term="my string")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_artist(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_artist()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_artist(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist?mbId=123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_artist(id_="123456")
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test__artist_json(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist/lookup?term=lidarr%3A123456-123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/qualityprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/metadataprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )

    data = lidarr_client._artist_json(
        id_="123456-123456",
        root_dir="/",
        quality_profile_id=1,
        metadata_profile_id=1,
        monitored=False,
        artist_monitor=LidarrArtistMonitor.FIRST_ALBUM,
        artist_search_for_missing_albums=False,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingProfile):
        data = lidarr_client._artist_json(id_="123456-123456", root_dir="/")
        assert False

    with contextlib.suppress(PyarrMissingProfile):
        data = lidarr_client._artist_json(
            id_="123456-123456", root_dir="/", quality_profile_id=1
        )
        assert False


@pytest.mark.usefixtures
def test_add_artist(responses, lidarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8686/api/v1/artist",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist.json"),
        status=201,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist/lookup?term=lidarr%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.add_artist(
        id_="123456",
        root_dir="/",
        quality_profile_id=1,
        metadata_profile_id=1,
        monitored=False,
        artist_monitor=LidarrArtistMonitor.LATEST_ALBUM,
        artist_search_for_missing_albums=False,
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_artist(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist.json"),
        status=202,
        match_querystring=True,
    )
    artist = lidarr_client.get_artist(1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/artist",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist.json"),
        status=202,
        match_querystring=True,
    )
    data = lidarr_client.upd_artist(data=artist)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_delete_artist(responses, lidarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/artist/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.delete_artist(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_album(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/album?includeAllArtistAlbums=False",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/album_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_album()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/album/1?includeAllArtistAlbums=False",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/album.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_album(albumIds=1)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/album?includeAllArtistAlbums=False&foreignAlbumId=123456-123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/album.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_album(foreignAlbumId="123456-123456")
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/album?includeAllArtistAlbums=False&albumids=1&albumids=2&albumids=3",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/album_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_album(albumIds=[1, 2, 3])
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/album?includeAllArtistAlbums=True&artistId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/album_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_album(artistId=1, allArtistAlbums=True)
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test__album_json(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/album/lookup?term=lidarr%3A123456-123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/qualityprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/metadataprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )

    data = lidarr_client._album_json(
        id_="123456-123456",
        root_dir="/",
        quality_profile_id=1,
        metadata_profile_id=1,
        monitored=False,
        artist_monitor=LidarrArtistMonitor.FIRST_ALBUM,
        artist_search_for_missing_albums=False,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingProfile):
        data = lidarr_client._album_json(id_="123456-123456", root_dir="/")
        assert False

    with contextlib.suppress(PyarrMissingProfile):
        data = lidarr_client._album_json(
            id_="123456-123456", root_dir="/", quality_profile_id=1
        )
        assert False


@pytest.mark.usefixtures
def test_add_album(responses, lidarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8686/api/v1/album",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/album.json"),
        status=201,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/album/lookup?term=lidarr%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.add_album(
        id_="123456",
        root_dir="/",
        quality_profile_id=1,
        metadata_profile_id=1,
        monitored=False,
        artist_monitor=LidarrArtistMonitor.LATEST_ALBUM,
        artist_search_for_missing_albums=False,
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_album(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/album/1?includeAllArtistAlbums=False",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/album.json"),
        status=202,
        match_querystring=True,
    )
    album = lidarr_client.get_album(1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/album",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/album.json"),
        status=202,
        match_querystring=True,
    )
    data = lidarr_client.upd_album(data=album)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_delete_album(responses, lidarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/album/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.delete_album(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_post_command(responses, lidarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8686/api/v1/command",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/command.json"),
        status=201,
        match_querystring=True,
    )

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


@pytest.mark.usefixtures
def test_get_wanted(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/wanted/missing",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/wanted_missing.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_wanted()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/wanted/cutoff",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/wanted_missing.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_wanted(missing=False)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/wanted/missing?page=2&pageSize=20&sortKey=albums.title&sortDirection=ascending",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/wanted_missing.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_wanted(
        page=2,
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
def test_get_parse(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/parse?title=test",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_parse(title="test")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_tracks(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/track?artistId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_tracks(artistId=1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/track?albumId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_tracks(albumId=1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/track?albumReleaseId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_tracks(albumReleaseId=1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/track?trackIds=1&trackIds=2&trackIds=3",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_tracks(trackIds=[1, 2, 3])
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/track/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_tracks(trackIds=1)
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_tracks()
        assert False


# TODO: confirm trackfile fixtures
@pytest.mark.usefixtures
def test_get_track_file(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile?artistId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_track_file(artistId=1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile?albumId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_track_file(albumId=1)
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile?trackFileIds=1&trackFileIds=2&trackFileIds=3",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_track_file(trackFileIds=[1, 2, 3])
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_track_file(trackFileIds=1)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile?unmapped=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_track_file(unmapped=True)
    assert isinstance(data, list)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_track_file()
        assert False


@pytest.mark.usefixtures
def test_upd_track_file(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/trackfile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track.json"),
        status=200,
        match_querystring=True,
    )
    track = lidarr_client.get_track_file(trackFileIds=1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/trackfile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/track.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.upd_track_file(data=track)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_delete_track_file(responses, lidarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/trackfile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.delete_track_file(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_metadata_profile(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/metadataprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/metadataprofile_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_metadata_profile()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/metadataprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/metadataprofile.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_metadata_profile(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_metadata_profile(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/metadataprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/metadataprofile.json"),
        status=200,
        match_querystring=True,
    )
    profile = lidarr_client.get_metadata_profile(id_=1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/metadataprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/metadataprofile.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.upd_metadata_profile(data=profile)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_metadata_provider(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/config/metadataProvider",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/metadataprovider.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_metadata_provider()
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_metadata_provider(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/config/metadataProvider",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/metadataprovider.json"),
        status=200,
        match_querystring=True,
    )
    provider = lidarr_client.get_metadata_provider()

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/config/metadataProvider",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/metadataprovider.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.upd_metadata_provider(data=provider)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_queue(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_queue()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue?page=1&pageSize=10&sortKey=timeleft&sortDirection=default",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_queue(
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
    data = lidarr_client.get_queue(
        unknown_artists=True, include_album=True, include_artist=True
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_queue(sort_key=LidarrSortKey.ARTIST_ID)
        assert False

    with contextlib.suppress(PyarrMissingArgument):
        data = lidarr_client.get_queue(sort_dir=PyarrSortDirection.ASC)
        assert False


# TODO: get correct fixture
@pytest.mark.usefixtures
def test_get_queue_details(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue/details",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_queue_details()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/queue/details?includeArtist=True&includeAlbum=True&artistId=1&albumIds=1&albumIds=2",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_queue_details(
        include_artist=True, include_album=True, artistId=1, albumIds=[1, 2]
    )
    assert isinstance(data, list)


# TODO: get correct fixture
@pytest.mark.usefixtures
def test_get_release(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/release",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_release()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/release?artistId=1&albumId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_release(artistId=1, albumId=1)
    assert isinstance(data, list)


# TODO: get correct fixture
@pytest.mark.usefixtures
def test_get_rename(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/rename?artistId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_rename(artistId=1)
    assert isinstance(data, list)
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/rename?artistId=1&albumId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_rename(artistId=1, albumId=1)
    assert isinstance(data, list)

    with contextlib.suppress(TypeError):
        data = lidarr_client.get_rename()
        assert False


# TODO: get correct fixture
@pytest.mark.usefixtures
def test_get_manual_import(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/manualimport?folder=/music/",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_manual_import(folder="/music/")
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/manualimport?folder=/music/&downloadId=1&artistId=1&filterExistingFiles=True&replaceExistingFiles=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_manual_import(
        folder="/music/",
        downloadId=1,
        artistId=1,
        filterExistingFiles=True,
        replaceExistingFiles=True,
    )
    assert isinstance(data, list)


# TODO: get correct fixture, confirm update returns dict
@pytest.mark.usefixtures
def test_upd_manual_import(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/manualimport?folder=/music/",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    man_import = lidarr_client.get_manual_import(folder="/music/")

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/manualimport",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_dict.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.upd_manual_import(data=man_import)
    assert isinstance(data, dict)


# TODO: get correct fixture
@pytest.mark.usefixtures
def test_get_manual_import(responses, lidarr_client):

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/retag",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_retag()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/retag?artistId=1&albumId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_list.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_retag(artistId=1, albumId=1)
    assert isinstance(data, list)
