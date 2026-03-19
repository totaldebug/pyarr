def test_sonarr_system_status(sonarr_client):
    status = sonarr_client.system.get_status()
    assert isinstance(status, dict)
    assert "version" in status
    assert status["appName"] == "Sonarr"


def test_sonarr_system_health(sonarr_client):
    health = sonarr_client.system.get_health()
    assert isinstance(health, list)


def test_sonarr_tag_get(sonarr_client):
    tags = sonarr_client.tag.get()
    assert isinstance(tags, list)


def test_sonarr_tag_create_update_delete(sonarr_client):
    # Create
    tag_name = "test_tag"
    new_tag = sonarr_client.tag.create(tag_name)
    assert new_tag["label"] == tag_name
    tag_id = new_tag["id"]

    # Update
    updated_name = "test_tag_updated"
    updated_tag = sonarr_client.tag.update(tag_id, updated_name)
    assert updated_tag["label"] == updated_name

    # Delete
    sonarr_client.tag.delete(tag_id)

    # Verify deletion
    tags = sonarr_client.tag.get()
    assert not any(t["id"] == tag_id for t in tags)
