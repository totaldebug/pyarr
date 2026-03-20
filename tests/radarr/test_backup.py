from pyarr.radarr import Radarr


def test_radarr_create_backup(radarr_client: Radarr):
    response = radarr_client.backup.create()
    assert response is not None
    assert isinstance(response, dict)
    assert response["commandName"] == "Backup"
    print(response)


def test_radarr_get_backup(radarr_client: Radarr):
    response = radarr_client.backup.get()
    assert response is not None
    assert isinstance(response, list)
    print(response)
