"""Which components each client exposes.

Regression tests for #192. The support lists come from probing live containers: Sonarr
4.0.19.2979 answers every media management component, Prowlarr 2.x answers a subset and
404s the rest, and Bazarr and Dispatcharr answer unsupported paths with a 200 and their
single page app HTML rather than a 404, which is what made the gap so hard to spot.
"""

import pytest

from pyarr import Bazarr, Dispatcharr, Lidarr, Prowlarr, Radarr, Readarr, Sonarr, Whisparr

MEDIA_COMPONENTS = [
    "backup",
    "blocklist",
    "calendar",
    "command",
    "download_client",
    "history",
    "import_list",
    "indexer",
    "log",
    "metadata",
    "notification",
    "quality_definition",
    "quality_profile",
    "queue",
    "remote_path_mapping",
    "root_folder",
    "tag",
    "update",
]

#: Components Prowlarr answers, verified against a live instance.
PROWLARR_SUPPORTED = ["backup", "command", "download_client", "history", "indexer", "log", "notification", "tag", "update"]

#: Components Prowlarr 404s.
PROWLARR_UNSUPPORTED = [c for c in MEDIA_COMPONENTS if c not in PROWLARR_SUPPORTED]


def _client(client_class, api_ver):
    """Builds a client without touching the network.

    Args:
        client_class: The client class to build.
        api_ver (str): API version, passed so the client skips auto detection.

    Returns:
        The constructed client.
    """
    return client_class(host="localhost", api_key="testkey", api_ver=api_ver, tls=False)


@pytest.mark.parametrize("client_class", [Sonarr, Radarr, Lidarr, Readarr, Whisparr])
@pytest.mark.parametrize("component", MEDIA_COMPONENTS)
def test_media_clients_expose_every_media_component(client_class, component):
    assert hasattr(_client(client_class, "v3"), component)


@pytest.mark.parametrize("component", PROWLARR_SUPPORTED)
def test_prowlarr_exposes_supported_components(component):
    assert hasattr(_client(Prowlarr, "v1"), component)


@pytest.mark.parametrize("component", PROWLARR_UNSUPPORTED)
def test_prowlarr_hides_unsupported_components(component):
    """Prowlarr answers these with a 404, so the attribute must not exist."""
    assert not hasattr(_client(Prowlarr, "v1"), component)


@pytest.mark.parametrize("client_class", [Bazarr, Dispatcharr])
@pytest.mark.parametrize("component", MEDIA_COMPONENTS)
def test_non_media_clients_hide_media_components(client_class, component):
    """Bazarr and Dispatcharr answer these with their HTML page, not JSON, so hide them."""
    assert not hasattr(_client(client_class, ""), component)


@pytest.mark.parametrize(
    "client_class, api_ver",
    [(Sonarr, "v3"), (Radarr, "v3"), (Lidarr, "v1"), (Readarr, "v1"), (Whisparr, "v3"), (Prowlarr, "v1"), (Bazarr, ""), (Dispatcharr, "")],
)
def test_every_client_exposes_system(client_class, api_ver):
    """system is the one component every client answers, Bazarr included."""
    assert hasattr(_client(client_class, api_ver), "system")


def test_bazarr_wanted_is_split_by_media_type():
    """Bazarr has no combined wanted endpoint - subtitles/wanted returned the HTML page."""
    client = _client(Bazarr, "")

    assert not hasattr(client, "wanted")
    assert client.wanted_episodes.path == "episodes/wanted"
    assert client.wanted_movies.path == "movies/wanted"
