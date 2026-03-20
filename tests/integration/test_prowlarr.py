def test_prowlarr_system_status(prowlarr_client):
    status = prowlarr_client.system.get_status()
    assert isinstance(status, dict)
    assert "version" in status
    assert status["appName"] == "Prowlarr"


def test_prowlarr_indexer(prowlarr_client):
    indexers = prowlarr_client.indexer.get()
    assert isinstance(indexers, list)

    schemas = prowlarr_client.indexer.get_schema()
    assert isinstance(schemas, list)
    assert len(schemas) > 0


def test_prowlarr_applications(prowlarr_client):
    apps = prowlarr_client.applications.get()
    assert isinstance(apps, list)


def test_prowlarr_search(prowlarr_client):
    # This might be empty if no indexers are configured, but should return a list
    results = prowlarr_client.search.get(query="test")
    assert isinstance(results, list)


def test_prowlarr_indexer_proxy(prowlarr_client):
    proxies = prowlarr_client.indexer_proxy.get()
    assert isinstance(proxies, list)
