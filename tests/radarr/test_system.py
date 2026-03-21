from pyarr import Radarr


def test_radarr_health(radarr_client: Radarr):
    response = radarr_client.system.get_health()
    assert response is not None
    assert isinstance(response, list)


def test_radarr_status(radarr_client: Radarr):
    response = radarr_client.system.get_status()
    assert response is not None
    assert isinstance(response, dict)


def test_radarr_diskspace(radarr_client: Radarr):
    response = radarr_client.system.get_diskspace()
    assert response is not None
    assert isinstance(response, list)


def test_get_task(radarr_client: Radarr):
    response = radarr_client.system.get_task()
    assert isinstance(response, list)

    response = radarr_client.system.get_task(response[0]["id"])
    assert isinstance(response, dict)


def test_request_restart(radarr_client: Radarr):
    response = radarr_client.system.request_restart()
    assert isinstance(response, dict)
    assert response["restarting"]
