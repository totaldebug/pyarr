import pytest

from pyarr.lidarr import Lidarr
from pyarr.radarr import Radarr
from pyarr.readarr import Readarr
from pyarr.sonarr import Sonarr

from . import (
    LIDARR_API_KEY,
    MOCK_API_KEY,
    MOCK_HOST,
    RADARR_API_KEY,
    READARR_API_KEY,
    SONARR_API_KEY,
)


@pytest.fixture()
def sonarr_client():
    with Sonarr(host="localhost", api_key=SONARR_API_KEY, tls=False) as client:
        yield client


@pytest.fixture(
    params=[
        (Lidarr, MOCK_HOST, MOCK_API_KEY),
        (Radarr, MOCK_HOST, MOCK_API_KEY),
        (Sonarr, MOCK_HOST, MOCK_API_KEY),
        (Readarr, MOCK_HOST, MOCK_API_KEY),
    ]
)
def client_mock(request):
    client_class, host, api_key = request.param
    with client_class(host=host, api_key=api_key, tls=False) as client:
        yield client


@pytest.fixture()
def radarr_client():
    with Radarr(host="localhost", api_key=RADARR_API_KEY, tls=False) as client:
        yield client


@pytest.fixture()
def lidarr_client():
    with Lidarr(host="localhost", api_key=LIDARR_API_KEY, tls=False) as client:
        yield client


@pytest.fixture()
def readarr_client():
    with Readarr(host="localhost", api_key=READARR_API_KEY, tls=False) as client:
        yield client
