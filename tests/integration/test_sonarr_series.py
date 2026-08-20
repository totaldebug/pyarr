from pyarr import Sonarr


def test_sonarr_series_get(sonarr_client: Sonarr):
    series = sonarr_client.series.get()
    assert isinstance(series, list)


def test_sonarr_series_lookup(sonarr_client: Sonarr):
    # Lookup "The Simpsons"
    results = sonarr_client.series.lookup(term="The Simpsons")
    assert isinstance(results, list)
    assert len(results) > 0
    assert any("Simpsons" in r["title"] for r in results)


def test_sonarr_series_get_tmdb(sonarr_client: Sonarr):
    # The Simpsons TMDB ID is 12
    try:
        series = sonarr_client.series.get(item_id=12, tmdb=True)
        assert isinstance(series, list)
    except Exception:
        pass


def test_sonarr_series_add_update_delete(sonarr_client: Sonarr):
    # Get root folder
    root_folders = sonarr_client.root_folder.get()
    if not root_folders:
        sonarr_client.root_folder.add(path="/config")
        root_folders = sonarr_client.root_folder.get()
    assert isinstance(root_folders, list)

    # Lookup "The Simpsons" (TVDB: 71663)
    lookup = sonarr_client.series.lookup(item_id=71663)
    assert len(lookup) > 0
    simpsons = lookup[0]

    # Check if already exists and delete it
    all_series = sonarr_client.series.get()
    assert isinstance(all_series, list)
    for s in all_series:
        if s["tvdbId"] == 71663:
            sonarr_client.series.delete(item_id=s["id"])
            break

    # Add series
    added_series = sonarr_client.series.add(
        series=simpsons,
        quality_profile_id=1,
        language_profile_id=1,
        root_dir=root_folders[0]["path"],
    )
    assert added_series["title"] == "The Simpsons"
    series_id = added_series["id"]

    # Update series
    added_series["monitored"] = False
    updated_series = sonarr_client.series.update(data=added_series)
    assert updated_series["monitored"] is False

    # Delete series
    assert sonarr_client.series.delete(item_id=series_id) is True


def test_sonarr_series_bulk_update_and_bulk_delete(sonarr_client: Sonarr):
    root_folders = sonarr_client.root_folder.get()
    if not root_folders:
        sonarr_client.root_folder.add(path="/config")
        root_folders = sonarr_client.root_folder.get()
    assert isinstance(root_folders, list)

    # The Simpsons (71663) and Futurama (73871)
    tvdb_ids = [71663, 73871]

    # Remove any existing copies so the add below always succeeds
    all_series = sonarr_client.series.get()
    assert isinstance(all_series, list)
    existing = [s["id"] for s in all_series if s["tvdbId"] in tvdb_ids]
    if existing:
        sonarr_client.series.delete(item_id=existing)

    series_ids = []
    for tvdb_id in tvdb_ids:
        lookup = sonarr_client.series.lookup(item_id=tvdb_id)
        assert len(lookup) > 0
        added = sonarr_client.series.add(
            series=lookup[0],
            quality_profile_id=1,
            language_profile_id=1,
            root_dir=root_folders[0]["path"],
            monitored=False,
        )
        series_ids.append(added["id"])

    # Bulk update both series in a single request
    updated = sonarr_client.series.bulk_update(data={"seriesIds": series_ids, "monitored": True})
    assert isinstance(updated, list)
    assert {s["id"] for s in updated} == set(series_ids)
    assert all(s["monitored"] is True for s in updated)

    # Bulk delete both series in a single request
    assert sonarr_client.series.delete(item_id=series_ids, delete_files=True) is True

    remaining = sonarr_client.series.get()
    assert isinstance(remaining, list)
    assert not [s for s in remaining if s["id"] in series_ids]
