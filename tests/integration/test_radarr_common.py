def test_radarr_system_status(radarr_client):
    status = radarr_client.system.get_status()
    assert isinstance(status, dict)
    assert "version" in status
    assert status["appName"] == "Radarr"


def test_radarr_tag_get(radarr_client):
    tags = radarr_client.tag.get()
    assert isinstance(tags, list)
