def test_sonarr_indexer(sonarr_client):
    indexers = sonarr_client.indexer.get()
    assert isinstance(indexers, list)

    schemas = sonarr_client.indexer.get_schema()
    assert isinstance(schemas, list)
    assert len(schemas) > 0


def test_sonarr_download_client(sonarr_client):
    clients = sonarr_client.download_client.get()
    assert isinstance(clients, list)

    schemas = sonarr_client.download_client.get_schema()
    assert isinstance(schemas, list)
    assert len(schemas) > 0


def test_sonarr_import_list(sonarr_client):
    lists = sonarr_client.import_list.get()
    assert isinstance(lists, list)

    schemas = sonarr_client.import_list.get_schema()
    assert isinstance(schemas, list)
    assert len(schemas) > 0


def test_sonarr_notification(sonarr_client):
    notifications = sonarr_client.notification.get()
    assert isinstance(notifications, list)

    schemas = sonarr_client.notification.get_schema()
    assert isinstance(schemas, list)
    assert len(schemas) > 0


def test_sonarr_quality_profile(sonarr_client):
    profiles = sonarr_client.quality_profile.get()
    assert isinstance(profiles, list)
    assert len(profiles) > 0

    schemas = sonarr_client.quality_profile.get_schema()
    assert isinstance(schemas, list | dict)


def test_radarr_quality_profile_schema(radarr_client):
    schemas = radarr_client.quality_profile.get_schema()
    assert isinstance(schemas, list | dict)


def test_lidarr_quality_profile_schema(lidarr_client):
    schemas = lidarr_client.quality_profile.get_schema()
    assert isinstance(schemas, list | dict)


def test_sonarr_quality_definition(sonarr_client):
    definitions = sonarr_client.quality_definition.get()
    assert isinstance(definitions, list)
    assert len(definitions) > 0


def test_sonarr_queue(sonarr_client):
    queue = sonarr_client.queue.get(page=1, page_size=10)
    assert isinstance(queue, dict)
    assert "records" in queue


def test_sonarr_remote_path_mapping(sonarr_client):
    mappings = sonarr_client.remote_path_mapping.get()
    assert isinstance(mappings, list)


def test_sonarr_command(sonarr_client):
    commands = sonarr_client.command.get()
    assert isinstance(commands, list)
