from pyarr.sonarr import Sonarr


def test_sonarr_create_backup(sonarr_client: Sonarr):
    response = sonarr_client.backup.create()
    assert response is not None
    assert isinstance(response, dict)
    assert response["commandName"] == "Backup"
    print(response)


def test_sonarr_get_backup(sonarr_client: Sonarr):
    response = sonarr_client.backup.get()
    assert response is not None
    assert isinstance(response, list)
    print(response)
