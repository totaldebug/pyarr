from pyarr.readarr import Readarr


def test_readarr_health(readarr_client: Readarr):
    response = readarr_client.system.get_health()
    assert response is not None
    assert isinstance(response, list)


def test_readarr_status(readarr_client: Readarr):
    response = readarr_client.system.get_status()
    assert response is not None
    assert isinstance(response, dict)


def test_radarr_diskspace(readarr_client: Readarr):
    response = readarr_client.system.get_diskspace()
    assert response is not None
    assert isinstance(response, list)


def test_get_task(readarr_client: Readarr):
    response = readarr_client.system.get_task()
    assert isinstance(response, list)

    response = readarr_client.system.get_task(response[0]["id"])
    assert isinstance(response, dict)


def test_request_restart(readarr_client: Readarr):
    response = readarr_client.system.request_restart()
    assert isinstance(response, dict)
    assert response["restarting"]
