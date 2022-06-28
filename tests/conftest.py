import pytest

from pyarr.sonarr import SonarrAPI

from tests import API_TOKEN, HOST_URL


@pytest.fixture()
def sonarr_client():
    yield SonarrAPI(f"{HOST_URL}:8989", API_TOKEN)
