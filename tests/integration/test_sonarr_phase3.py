def test_sonarr_episode(sonarr_client):
    series = sonarr_client.series.get()
    if not series:
        # Add a series for testing (The Simpsons)
        lookup = sonarr_client.series.lookup(term="tvdb:71663")
        sonarr_client.series.add(
            series=lookup[0],
            quality_profile_id=1,
            language_profile_id=1,
            root_dir="/config",
        )
        series = sonarr_client.series.get()

    series_id = series[0]["id"]
    episodes = sonarr_client.episode.get(series_id=series_id)
    assert isinstance(episodes, list)
    assert len(episodes) > 0

    episode_id = episodes[0]["id"]
    episode = sonarr_client.episode.get(item_id=episode_id)
    assert isinstance(episode, dict)
    assert episode["id"] == episode_id


def test_sonarr_episode_file(sonarr_client):
    series = sonarr_client.series.get()
    if series:
        series_id = series[0]["id"]
        files = sonarr_client.episode_file.get(series_id=series_id)
        assert isinstance(files, list)


def test_sonarr_release(sonarr_client):
    series = sonarr_client.series.get()
    if series:
        episodes = sonarr_client.episode.get(series_id=series[0]["id"])
        if episodes:
            releases = sonarr_client.release.get(episode_id=episodes[0]["id"])
            assert isinstance(releases, list)


def test_sonarr_manual_import(sonarr_client):
    # This might return empty but should be a list
    imports = sonarr_client.manual_import.get(folder="/config")
    assert isinstance(imports, list)
