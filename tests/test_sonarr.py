from warnings import warn

import pytest

from tests import load_fixture


@pytest.mark.usefixtures
def test_get_episode(responses, sonarr_client):
    """Test getting episode"""
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode/0",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episode.json"),
        status=200,
    )
    data = sonarr_client.get_episode(0)

    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode?seriesId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series.json"),
        status=200,
    )
    data = sonarr_client.get_episode(1, True)
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_episodes_by_series_id(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode?seriesId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/series.json"),
        status=200,
    )
    data = sonarr_client.get_episodes_by_series_id(1)
    with pytest.warns(DeprecationWarning):
        warn(
            "This method is deprecated and will be removed in a future release. Please use get_episode()",
            DeprecationWarning,
            stacklevel=2,
        )
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_episode_by_episode_id(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episode/0",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episode.json"),
        status=200,
    )
    data = sonarr_client.get_episode_by_episode_id(0)
    with pytest.warns(DeprecationWarning):
        warn(
            "This method is deprecated and will be removed in a future release. Please use get_episode()",
            DeprecationWarning,
            stacklevel=2,
        )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_episode(responses, sonarr_client):
    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/episode/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/updated_episode.json"),
        status=200,
    )
    payload = {"monitored": True}
    data = sonarr_client.upd_episode(1, payload)

    assert isinstance(data, dict)
    assert data["monitored"] == True
