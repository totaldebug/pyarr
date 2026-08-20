from unittest.mock import AsyncMock, MagicMock

import pytest

from pyarr._async.common.import_list_exclusion import ImportListExclusion as AsyncImportListExclusion
from pyarr._async.lidarr import Lidarr as AsyncLidarr
from pyarr._async.radarr import Radarr as AsyncRadarr
from pyarr._async.readarr import Readarr as AsyncReadarr
from pyarr._async.sonarr import Sonarr as AsyncSonarr
from pyarr._async.utils.http import RequestHandler as AsyncRequestHandler
from pyarr._async.whisparr import Whisparr as AsyncWhisparr
from pyarr._sync.common.import_list_exclusion import ImportListExclusion
from pyarr._sync.lidarr import Lidarr
from pyarr._sync.radarr import Radarr
from pyarr._sync.readarr import Readarr
from pyarr._sync.sonarr import Sonarr
from pyarr._sync.utils.http import RequestHandler
from pyarr._sync.whisparr import Whisparr

RADARR_EXCLUSION = {"tmdbId": 603, "movieTitle": "The Matrix", "movieYear": 1999}
SONARR_EXCLUSION = {"tvdbId": 78804, "title": "Doctor Who", "year": 2005}


def test_import_list_exclusion_get_all():
    """The exclusion list is served from the module path with no item id."""
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = [RADARR_EXCLUSION | {"id": 1}]
    exclusion = ImportListExclusion(mock_handler, path="exclusions")

    assert exclusion.get() == [RADARR_EXCLUSION | {"id": 1}]
    mock_handler.request.assert_called_once_with("exclusions", params=None)


def test_import_list_exclusion_get_by_id():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = RADARR_EXCLUSION | {"id": 1}
    exclusion = ImportListExclusion(mock_handler, path="exclusions")

    assert exclusion.get(1) == RADARR_EXCLUSION | {"id": 1}
    mock_handler.request.assert_called_once_with("exclusions/1", params=None)


def test_import_list_exclusion_add():
    """The add payload is posted as the request body."""
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = SONARR_EXCLUSION | {"id": 1}
    exclusion = ImportListExclusion(mock_handler)

    assert exclusion.add(SONARR_EXCLUSION) == SONARR_EXCLUSION | {"id": 1}
    mock_handler.request.assert_called_once_with("importlistexclusion", method="POST", json_data=SONARR_EXCLUSION)


def test_import_list_exclusion_add_rejects_non_dict_response():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    exclusion = ImportListExclusion(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        exclusion.add(SONARR_EXCLUSION)


def test_import_list_exclusion_delete():
    mock_handler = MagicMock(spec=RequestHandler)
    exclusion = ImportListExclusion(mock_handler, path="exclusions")

    assert exclusion.delete(1) is None
    mock_handler.request.assert_called_once_with("exclusions/1", method="DELETE")


@pytest.mark.parametrize(
    ("client_class", "expected_path"),
    [
        (Radarr, "exclusions"),
        (Sonarr, "importlistexclusion"),
        (Lidarr, "importlistexclusion"),
        (Readarr, "importlistexclusion"),
        (Whisparr, "importlistexclusion"),
    ],
)
def test_client_wires_the_verified_endpoint(client_class, expected_path):
    """Radarr serves exclusions from `exclusions`, every other client from `importlistexclusion`."""
    client = client_class(host="localhost", api_key="key", tls=False, api_ver="v3")

    assert client.import_list_exclusion.path == expected_path


@pytest.mark.asyncio
async def test_async_import_list_exclusion_get_all():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = [RADARR_EXCLUSION | {"id": 1}]
    exclusion = AsyncImportListExclusion(mock_handler, path="exclusions")

    assert await exclusion.get() == [RADARR_EXCLUSION | {"id": 1}]
    mock_handler.request.assert_called_once_with("exclusions", params=None)


@pytest.mark.asyncio
async def test_async_import_list_exclusion_get_by_id():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = RADARR_EXCLUSION | {"id": 1}
    exclusion = AsyncImportListExclusion(mock_handler, path="exclusions")

    assert await exclusion.get(1) == RADARR_EXCLUSION | {"id": 1}
    mock_handler.request.assert_called_once_with("exclusions/1", params=None)


@pytest.mark.asyncio
async def test_async_import_list_exclusion_add():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = SONARR_EXCLUSION | {"id": 1}
    exclusion = AsyncImportListExclusion(mock_handler)

    assert await exclusion.add(SONARR_EXCLUSION) == SONARR_EXCLUSION | {"id": 1}
    mock_handler.request.assert_called_once_with("importlistexclusion", method="POST", json_data=SONARR_EXCLUSION)


@pytest.mark.asyncio
async def test_async_import_list_exclusion_add_rejects_non_dict_response():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = []
    exclusion = AsyncImportListExclusion(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        await exclusion.add(SONARR_EXCLUSION)


@pytest.mark.asyncio
async def test_async_import_list_exclusion_delete():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    exclusion = AsyncImportListExclusion(mock_handler, path="exclusions")

    assert await exclusion.delete(1) is None
    mock_handler.request.assert_called_once_with("exclusions/1", method="DELETE")


@pytest.mark.parametrize(
    ("client_class", "expected_path"),
    [
        (AsyncRadarr, "exclusions"),
        (AsyncSonarr, "importlistexclusion"),
        (AsyncLidarr, "importlistexclusion"),
        (AsyncReadarr, "importlistexclusion"),
        (AsyncWhisparr, "importlistexclusion"),
    ],
)
def test_async_client_wires_the_verified_endpoint(client_class, expected_path):
    client = client_class(host="localhost", api_key="key", tls=False, api_ver="v3")

    assert client.import_list_exclusion.path == expected_path
