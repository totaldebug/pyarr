import pytest

from pyarr._async.common.system import MediaSystem, System
from pyarr._async.lidarr import Lidarr
from pyarr._async.prowlarr import Prowlarr
from pyarr._async.radarr import Radarr
from pyarr._async.readarr import Readarr
from pyarr._async.sonarr import Sonarr
from pyarr._async.whisparr import Whisparr


def _client(cls, api_ver):
    return cls(host="127.0.0.1", api_key="123456789abcdefg123456789", tls=False, api_ver=api_ver)


@pytest.mark.parametrize(
    ("cls", "api_ver"),
    [(Sonarr, "v3"), (Radarr, "v3"), (Lidarr, "v1"), (Readarr, "v1"), (Whisparr, "v3")],
)
def test_media_clients_report_diskspace(cls, api_ver):
    client = _client(cls, api_ver)
    assert isinstance(client.system, MediaSystem)
    assert hasattr(client.system, "get_diskspace")


def test_prowlarr_does_not_report_diskspace():
    """Prowlarr manages no media and has no diskspace route; the call raised a 404."""
    client = _client(Prowlarr, "v1")

    assert isinstance(client.system, System)
    assert not isinstance(client.system, MediaSystem)
    assert not hasattr(client.system, "get_diskspace")


def test_prowlarr_keeps_the_rest_of_the_shared_system_surface():
    """Everything else on System is served by Prowlarr, so it must stay available."""
    client = _client(Prowlarr, "v1")

    for method in ("get_status", "get_health", "get_task", "get_routes", "request_restart"):
        assert hasattr(client.system, method), f"Prowlarr should still expose system.{method}"
