from pyarr import Readarr


def test_readarr_create_backup(readarr_client: Readarr):
    response = readarr_client.backup.create()
    assert response is not None
    assert isinstance(response, dict)
    assert response["commandName"] == "Backup"
    print(response)


def test_readarr_get_backup(readarr_client: Readarr):
    response = readarr_client.backup.get()
    assert response is not None
    assert isinstance(response, list)
    print(response)
