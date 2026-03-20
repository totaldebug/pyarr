def test_lidarr_system_status(lidarr_client):
    status = lidarr_client.system.get_status()
    assert isinstance(status, dict)
    assert "version" in status
    assert status["appName"] == "Lidarr"


def test_lidarr_tag_get(lidarr_client):
    tags = lidarr_client.tag.get()
    assert isinstance(tags, list)
