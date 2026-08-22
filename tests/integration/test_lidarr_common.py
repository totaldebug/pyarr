def test_lidarr_system_status(lidarr_client):
    status = lidarr_client.system.get_status()
    assert isinstance(status, dict)
    assert "version" in status
    assert status["appName"] == "Lidarr"


def test_lidarr_tag_get(lidarr_client):
    tags = lidarr_client.tag.get()
    assert isinstance(tags, list)


def test_lidarr_metadata_profile_get(lidarr_client):
    profiles = lidarr_client.metadata_profile.get()
    assert isinstance(profiles, list)
    assert profiles, "Lidarr ships with Standard and None profiles"
    for profile in profiles:
        assert "id" in profile
        assert "name" in profile
        # The fields that distinguish a Lidarr profile from a Readarr one.
        assert "primaryAlbumTypes" in profile
        assert "secondaryAlbumTypes" in profile
        assert "releaseStatuses" in profile


def test_lidarr_metadata_profile_get_by_id(lidarr_client):
    profiles = lidarr_client.metadata_profile.get()
    profile = lidarr_client.metadata_profile.get(item_id=profiles[0]["id"])
    assert isinstance(profile, dict)
    assert profile["id"] == profiles[0]["id"]
    assert profile["name"] == profiles[0]["name"]


def test_lidarr_metadata_profile_get_schema(lidarr_client):
    schema = lidarr_client.metadata_profile.get_schema()
    assert isinstance(schema, dict)
    assert "primaryAlbumTypes" in schema
    assert "secondaryAlbumTypes" in schema
    assert "releaseStatuses" in schema


def test_lidarr_metadata_profile_add_update_delete(lidarr_client):
    """Full round trip. Lidarr wants the complete album-type set, so clone one."""
    existing = lidarr_client.metadata_profile.get()
    payload = {k: v for k, v in existing[0].items() if k != "id"}
    payload["name"] = "pyarr-integration-test"

    added = lidarr_client.metadata_profile.add(payload)
    assert isinstance(added, dict)
    assert added["name"] == "pyarr-integration-test"
    profile_id = added["id"]

    try:
        added["name"] = "pyarr-integration-renamed"
        updated = lidarr_client.metadata_profile.update(profile_id, added)
        assert isinstance(updated, dict)
        assert updated["name"] == "pyarr-integration-renamed"
        assert updated["id"] == profile_id
    finally:
        lidarr_client.metadata_profile.delete(profile_id)

    remaining = [p["id"] for p in lidarr_client.metadata_profile.get()]
    assert profile_id not in remaining
