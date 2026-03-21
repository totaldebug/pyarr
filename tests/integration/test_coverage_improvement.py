from datetime import datetime
from unittest.mock import patch

import pytest

from pyarr import PyarrMissingArgument, PyarrResourceNotFound


def test_sonarr_download_client_extended(sonarr_client):
    # Test get with ID
    clients = sonarr_client.download_client.get()
    if len(clients) > 0:
        client_id = clients[0]["id"]
        client = sonarr_client.download_client.get(client_id)
        assert isinstance(client, dict)
        assert client["id"] == client_id

    # Test get_schema with implementation
    schemas = sonarr_client.download_client.get_schema()
    assert len(schemas) > 0
    impl = schemas[0]["implementation"]
    schema = sonarr_client.download_client.get_schema(implementation=impl)
    assert isinstance(schema, list)
    assert len(schema) > 0
    assert schema[0]["implementation"] == impl

    # Test ValueError paths using mocks
    with patch.object(sonarr_client.download_client.handler, "request", return_value="not a list"):
        with pytest.raises(ValueError, match="Expected a list response"):
            sonarr_client.download_client.get_schema()

    with patch.object(sonarr_client.download_client.handler, "request", return_value="not a dict"):
        with pytest.raises(ValueError, match="Expected a dictionary response"):
            sonarr_client.download_client.add({})

    with patch.object(sonarr_client.download_client.handler, "request", return_value="not a dict"):
        with pytest.raises(ValueError, match="Expected a dictionary response"):
            sonarr_client.download_client.update(1, {})


def test_sonarr_import_list_extended(sonarr_client):
    # Test get with ID
    lists = sonarr_client.import_list.get()
    if len(lists) > 0:
        list_id = lists[0]["id"]
        ilist = sonarr_client.import_list.get(list_id)
        assert isinstance(ilist, dict)
        assert ilist["id"] == list_id

    schemas = sonarr_client.import_list.get_schema()
    assert len(schemas) > 0
    impl = schemas[0]["implementation"]
    schema = sonarr_client.import_list.get_schema(implementation=impl)
    assert isinstance(schema, list)

    # Test ValueError paths using mocks
    with patch.object(sonarr_client.import_list.handler, "request", return_value="not a list"):
        with pytest.raises(ValueError, match="Expected a list response"):
            sonarr_client.import_list.get_schema()

    with patch.object(sonarr_client.import_list.handler, "request", return_value="not a dict"):
        with pytest.raises(ValueError, match="Expected a dictionary response"):
            sonarr_client.import_list.add({})

    with patch.object(sonarr_client.import_list.handler, "request", return_value="not a dict"):
        with pytest.raises(ValueError, match="Expected a dictionary response"):
            sonarr_client.import_list.update(1, {})


def test_sonarr_notification_extended(sonarr_client):
    # Test get with ID
    notifications = sonarr_client.notification.get()
    if len(notifications) > 0:
        notif_id = notifications[0]["id"]
        notif = sonarr_client.notification.get(notif_id)
        assert isinstance(notif, dict)
        assert notif["id"] == notif_id

    schemas = sonarr_client.notification.get_schema()
    assert len(schemas) > 0
    impl = schemas[0]["implementation"]
    schema = sonarr_client.notification.get_schema(implementation=impl)
    assert isinstance(schema, list)

    # Test ValueError paths using mocks
    with patch.object(sonarr_client.notification.handler, "request", return_value="not a list"):
        with pytest.raises(ValueError, match="Expected a list response"):
            sonarr_client.notification.get_schema()

    with patch.object(sonarr_client.notification.handler, "request", return_value="not a dict"):
        with pytest.raises(ValueError, match="Expected a dictionary response"):
            sonarr_client.notification.add({})

    with patch.object(sonarr_client.notification.handler, "request", return_value="not a dict"):
        with pytest.raises(ValueError, match="Expected a dictionary response"):
            sonarr_client.notification.update(1, {})


def test_sonarr_quality_profile_extended(sonarr_client):
    # Test get with ID
    profiles = sonarr_client.quality_profile.get()
    if len(profiles) > 0:
        profile_id = profiles[0]["id"]
        profile = sonarr_client.quality_profile.get(profile_id)
        assert isinstance(profile, dict)
        assert profile["id"] == profile_id

    # Test ValueError paths using mocks
    with patch.object(sonarr_client.quality_profile.handler, "request", return_value=1):
        with pytest.raises(ValueError, match="Expected a list or dictionary response"):
            sonarr_client.quality_profile.get_schema()

    with patch.object(sonarr_client.quality_profile.handler, "request", return_value="not a dict"):
        with pytest.raises(ValueError, match="Expected a dictionary response"):
            sonarr_client.quality_profile.add({})

    with patch.object(sonarr_client.quality_profile.handler, "request", return_value="not a dict"):
        with pytest.raises(ValueError, match="Expected a dictionary response"):
            sonarr_client.quality_profile.update(1, {})


def test_sonarr_queue_extended(sonarr_client):
    # Test missing argument exception
    with pytest.raises(PyarrMissingArgument):
        sonarr_client.queue.get(sort_key="title")

    with pytest.raises(PyarrMissingArgument):
        sonarr_client.queue.get(sort_dir="ascending")

    # Test kwargs
    res = sonarr_client.queue.get(unknown_param="test")
    assert isinstance(res, dict)

    # Test TypeError
    with patch.object(sonarr_client.queue.handler, "request", return_value=[]):
        with pytest.raises(TypeError, match="Expected response to be a dictionary"):
            sonarr_client.queue.get()

    # Test delete with all params
    try:
        sonarr_client.queue.delete(
            999,
            remove_from_client=True,
            blocklist=True,
            skip_redundant_dictionary_check=True,
            mark_as_failed=True,
            message="test",
        )
    except PyarrResourceNotFound:
        pass

    # Test bulk_delete with all params
    try:
        sonarr_client.queue.bulk_delete([998, 999], remove_from_client=True, blocklist=True)
    except Exception:
        pass


def test_sonarr_release_extended(sonarr_client):
    # get()
    releases = sonarr_client.release.get()
    assert isinstance(releases, list)

    # Get a real episode ID
    series = sonarr_client.release.handler.request("series")
    if not series:
        # Add a series for testing
        root_folders = sonarr_client.root_folder.get()
        if not root_folders:
            sonarr_client.root_folder.add(path="/config")
            root_folders = sonarr_client.root_folder.get()

        lookup = sonarr_client.series.lookup(item_id=71663)
        sonarr_client.series.add(
            series=lookup[0],
            quality_profile_id=1,
            language_profile_id=1,
            root_dir=root_folders[0]["path"],
        )
        series = sonarr_client.series.get()

    series_id = series[0]["id"]
    episodes = sonarr_client.episode.get(series_id=series_id)
    episode_id = episodes[0]["id"]

    # get(episode_id)
    releases = sonarr_client.release.get(episode_id=episode_id)
    assert isinstance(releases, list)

    # Test ValueError paths
    with patch.object(sonarr_client.release.handler, "request", return_value={}):
        with pytest.raises(ValueError, match="Expected a list response"):
            sonarr_client.release.get()

    with patch.object(sonarr_client.release.handler, "request", return_value=[]):
        with pytest.raises(ValueError, match="Expected a dictionary response"):
            sonarr_client.release.add("guid", 1)

    with patch.object(sonarr_client.release.handler, "request", return_value={}):
        with pytest.raises(ValueError, match="Expected a list response"):
            sonarr_client.release.push("title", "url", "Torrent", datetime.now())


def test_radarr_release_extended(radarr_client):
    # get()
    releases = radarr_client.release.get()
    assert isinstance(releases, list)

    # Get a real movie ID
    movies = radarr_client.movie.get()
    if not movies:
        # Add a movie for testing
        root_folders = radarr_client.root_folder.get()
        if not root_folders:
            radarr_client.root_folder.add(path="/config")
            root_folders = radarr_client.root_folder.get()

        lookup = radarr_client.movie.lookup(term="tmdb:12")  # Finding Nemo
        radarr_client.movie.add(
            movie=lookup[0],
            quality_profile_id=1,
            root_dir=root_folders[0]["path"],
        )
        movies = radarr_client.movie.get()

    movie_id = movies[0]["id"]

    # get(movie_id)
    releases = radarr_client.release.get(movie_id=movie_id)
    assert isinstance(releases, list)

    # Test ValueError paths
    with patch.object(radarr_client.release.handler, "request", return_value={}):
        with pytest.raises(ValueError, match="Expected a list response"):
            radarr_client.release.get()

    with patch.object(radarr_client.release.handler, "request", return_value=[]):
        with pytest.raises(ValueError, match="Expected a dictionary response"):
            radarr_client.release.add("guid", 1)

    with patch.object(radarr_client.release.handler, "request", return_value={}):
        with pytest.raises(ValueError, match="Expected a list response"):
            radarr_client.release.push("title", "url", "Torrent", datetime.now())
