from datetime import datetime, timedelta


def test_sonarr_calendar(sonarr_client):
    # Test without dates
    cal = sonarr_client.calendar.get()
    assert isinstance(cal, list)

    # Test with dates
    start = datetime.now()
    end = start + timedelta(days=7)
    cal = sonarr_client.calendar.get(start_date=start, end_date=end)
    assert isinstance(cal, list)

    # Test with kwargs
    cal = sonarr_client.calendar.get(includeSeries=True)
    assert isinstance(cal, list)


def test_sonarr_wanted(sonarr_client):
    wanted = sonarr_client.wanted.get(page=1, page_size=10)
    assert isinstance(wanted, dict)
    assert "records" in wanted


def test_sonarr_root_folder(sonarr_client):
    root_folders = sonarr_client.root_folder.get()
    if not root_folders:
        sonarr_client.root_folder.add(path="/config")
        root_folders = sonarr_client.root_folder.get()

    assert isinstance(root_folders, list)
    assert len(root_folders) > 0

    # Test with ID
    folder_id = root_folders[0]["id"]
    folder = sonarr_client.root_folder.get(folder_id)
    assert isinstance(folder, dict)
    assert folder["id"] == folder_id


def test_sonarr_update(sonarr_client):
    updates = sonarr_client.update.get()
    assert isinstance(updates, list)


def test_sonarr_metadata(sonarr_client):
    metadata = sonarr_client.metadata.get()
    assert isinstance(metadata, list)


def test_sonarr_log(sonarr_client):
    logs = sonarr_client.log.get(page=1, page_size=10)
    assert isinstance(logs, dict)
    assert "records" in logs
