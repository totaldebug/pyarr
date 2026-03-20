from pyarr.sonarr import Sonarr


def test_sonarr_health(sonarr_client: Sonarr):
    response = sonarr_client.system.get_health()
    assert response is not None
    assert isinstance(response, list)


def test_sonarr_status(sonarr_client: Sonarr):
    response = sonarr_client.system.get_status()
    assert response is not None
    assert isinstance(response, dict)


def test_radarr_diskspace(sonarr_client: Sonarr):
    response = sonarr_client.system.get_diskspace()
    assert response is not None
    assert isinstance(response, list)


def test_get_task(sonarr_client: Sonarr):
    response = sonarr_client.system.get_task()
    assert isinstance(response, list)

    response = sonarr_client.system.get_task(response[0]["id"])
    assert isinstance(response, dict)


def test_request_restart(sonarr_client: Sonarr):
    response = sonarr_client.system.request_restart()
    assert isinstance(response, dict)
    assert response["restarting"]
