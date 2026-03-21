from pyarr import Radarr


def test_radarr_tag(radarr_client: Radarr):
    # Create a tag
    tag = radarr_client.tag.create(label="test-tag")
    assert tag["label"] == "test-tag"
    assert "id" in tag

    # Get all tags
    tags = radarr_client.tag.get()
    assert isinstance(tags, list)
    assert any(t["id"] == tag["id"] for t in tags)

    # Get specific tag
    specific_tag = radarr_client.tag.get(item_id=tag["id"])
    assert specific_tag["id"] == tag["id"]
    assert specific_tag["label"] == "test-tag"

    # Get tag detail
    tag_detail = radarr_client.tag.get_detail(item_id=tag["id"])
    assert tag_detail["id"] == tag["id"]

    # Update tag
    updated_tag = radarr_client.tag.update(item_id=tag["id"], label="updated-tag")
    assert updated_tag["label"] == "updated-tag"

    # Delete tag
    radarr_client.tag.delete(tag["id"])
    tags_after_delete = radarr_client.tag.get()
    assert not any(t["id"] == tag["id"] for t in tags_after_delete)
