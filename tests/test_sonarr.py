from warnings import warn

import pytest

from pyarr.models.common import PyarrSortDirection
from pyarr.models.sonarr import SonarrSortKeys

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
        body=load_fixture("sonarr/episode_series.json"),
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
        body=load_fixture("sonarr/episode_series.json"),
        status=200,
    )
    data = sonarr_client.get_episodes_by_series_id(1)

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

    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_episode(responses, sonarr_client):
    responses.add(
        responses.PUT,
        "https://127.0.0.1:8989/api/v3/episode/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episode_update.json"),
        status=200,
    )
    payload = {"monitored": True}
    data = sonarr_client.upd_episode(1, payload)

    assert isinstance(data, dict)
    assert data["monitored"] == True


@pytest.mark.usefixtures
def test_get_episode_files_by_series_id(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile?seriesId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episodefile_series.json"),
        status=200,
    )
    data = sonarr_client.get_episode_files_by_series_id(1)

    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_episode_file(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episodefile.json"),
        status=200,
    )
    data = sonarr_client.get_episode_file(1)

    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_episode_file(responses, sonarr_client):
    """Test getting episode"""
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile/0",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episodefile.json"),
        status=200,
    )
    data = sonarr_client.get_episode_file(0)

    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/episodefile?seriesId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/episodefile_series.json"),
        status=200,
    )
    data = sonarr_client.get_episode_file(1, True)
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_del_episode_file(responses, sonarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8989/api/v3/episodefile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/delete.json"),
        status=200,
    )
    data = sonarr_client.del_episode_file(1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_wanted(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/wanted/missing?sortKey=airDateUtc&page=1&pageSize=10&sortDirection=default",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/wanted_missing.json"),
        status=200,
    )
    data = sonarr_client.get_wanted()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/wanted/missing?sortKey=airDateUtc&page=1&pageSize=10&sortDirection=default&includeSeries=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/wanted_missing_extended.json"),
        status=200,
    )
    data = sonarr_client.get_wanted(include_series=True)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/wanted/missing?sortKey=series.sortTitle&page=2&pageSize=20&sortDirection=ascending",
        headers={"Content-Type": "application/json"},
        body=load_fixture("sonarr/wanted_missing.json"),
        status=200,
    )
    data = sonarr_client.get_wanted(
        sort_key=SonarrSortKeys.SERIES_TITLE,
        page=2,
        page_size=20,
        sort_direction=PyarrSortDirection.ASC,
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_get_quality_profile(responses, sonarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualityprofile",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/qualityprofileall.json"),
        status=200,
    )
    data = sonarr_client.get_quality_profile()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8989/api/v3/qualityprofile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/qualityprofile.json"),
        status=200,
    )
    data = sonarr_client.get_quality_profile(1)
    assert isinstance(data, dict)
