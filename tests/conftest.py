import pytest

from pyarr.lidarr import LidarrAPI
from pyarr.radarr import RadarrAPI
from pyarr.readarr import ReadarrAPI
from pyarr.sonarr import SonarrAPI

from tests import API_TOKEN, HOST_URL


@pytest.fixture()
def sonarr_client():
    yield SonarrAPI(f"{HOST_URL}:8989", API_TOKEN)


@pytest.fixture()
def radarr_client():
    yield RadarrAPI(f"{HOST_URL}:7878", API_TOKEN)


@pytest.fixture()
def lidarr_client():
    yield LidarrAPI(f"{HOST_URL}:8686", API_TOKEN)


@pytest.fixture()
def readarr_client():
    yield ReadarrAPI(f"{HOST_URL}:8787", API_TOKEN)
