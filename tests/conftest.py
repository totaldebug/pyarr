import pytest

from pyarr.lidarr import LidarrAPI
from pyarr.radarr import RadarrAPI
from pyarr.readarr import ReadarrAPI
from pyarr.sonarr import SonarrAPI

from tests import (
    LIDARR_API_KEY,
    MOCK_API_KEY,
    MOCK_URL,
    RADARR_API_KEY,
    READARR_API_KEY,
    SONARR_API_KEY,
)


@pytest.fixture()
def sonarr_client():
    yield SonarrAPI("http://sonarr:8989", SONARR_API_KEY)


@pytest.fixture()
def sonarr_mock_client():
    yield SonarrAPI(f"{MOCK_URL}:8989", MOCK_API_KEY)


@pytest.fixture()
def radarr_client():
    yield RadarrAPI("http://radarr:7878", RADARR_API_KEY)


@pytest.fixture()
def radarr_mock_client():
    yield RadarrAPI(f"{MOCK_URL}:7878", MOCK_API_KEY)


@pytest.fixture()
def lidarr_client():
    yield LidarrAPI("http://lidarr:8686", LIDARR_API_KEY)


@pytest.fixture()
def lidarr_mock_client():
    yield LidarrAPI(f"{MOCK_URL}:8686", MOCK_API_KEY)


@pytest.fixture()
def readarr_client():
    yield ReadarrAPI("http://readarr:8787", READARR_API_KEY)


@pytest.fixture()
def readarr_mock_client():
    yield ReadarrAPI(f"{MOCK_URL}:8787", MOCK_API_KEY)
