from pyarr import Sonarr


def test_sonarr_episode(sonarr_client: Sonarr):
    # Get all series
    series = sonarr_client.series.get()
    if not series:
        # Add a series for testing
        root_folders = sonarr_client.root_folder.get()
        if not root_folders:
            sonarr_client.root_folder.add(path="/config")
            root_folders = sonarr_client.root_folder.get()

        lookup = sonarr_client.series.lookup(item_id=71663)
        sonarr_client.series.add(
            series=lookup[0],
            quality_profile_id=1,
            language_profile_id=1,
            root_dir=root_folders[0]["path"],
        )
        series = sonarr_client.series.get()

    series_id = series[0]["id"]

    # Get episodes for series
    episodes = sonarr_client.episode.get(series_id=series_id)
    assert isinstance(episodes, list)
    assert len(episodes) > 0

    episode_id = episodes[0]["id"]

    # Get specific episode
    episode = sonarr_client.episode.get(item_id=episode_id)
    assert isinstance(episode, dict)
    assert episode["id"] == episode_id

    # Update episode
    episode["monitored"] = not episode["monitored"]
    updated_episode = sonarr_client.episode.update(item_id=episode_id, data=episode)
    assert updated_episode["monitored"] == episode["monitored"]

    # Monitor episodes
    result = sonarr_client.episode.monitor(episode_ids=[episode_id], monitored=True)
    assert isinstance(result, list)
    assert result[0]["monitored"] is True
