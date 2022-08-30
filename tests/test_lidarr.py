import contextlib

import pytest

from pyarr.exceptions import PyarrMissingProfile
from pyarr.models.lidarr import LidarrArtistMonitor, LidarrCommand

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
