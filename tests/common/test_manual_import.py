from unittest.mock import AsyncMock, MagicMock

import pytest

from pyarr._async.lidarr.manual_import import ManualImport as AsyncLidarrManualImport
from pyarr._async.radarr.manual_import import ManualImport as AsyncRadarrManualImport
from pyarr._async.readarr.manual_import import ManualImport as AsyncReadarrManualImport
from pyarr._async.sonarr.manual_import import ManualImport as AsyncSonarrManualImport
from pyarr._async.utils.http import RequestHandler as AsyncRequestHandler
from pyarr._sync.lidarr.manual_import import ManualImport as LidarrManualImport
from pyarr._sync.radarr.manual_import import ManualImport as RadarrManualImport
from pyarr._sync.readarr.manual_import import ManualImport as ReadarrManualImport
from pyarr._sync.sonarr.manual_import import ManualImport as SonarrManualImport
from pyarr._sync.utils.http import RequestHandler

SYNC_CLASSES = [SonarrManualImport, RadarrManualImport, LidarrManualImport, ReadarrManualImport]
ASYNC_CLASSES = [
    AsyncSonarrManualImport,
    AsyncRadarrManualImport,
    AsyncLidarrManualImport,
    AsyncReadarrManualImport,
]


@pytest.mark.parametrize("manual_import_class", SYNC_CLASSES)
def test_manual_import_update_posts_a_list(manual_import_class):
    """Regression test for #165.

    manualimport only accepts POST - a PUT is answered with 405 Method Not Allowed - and it
    takes and returns a JSON array rather than a single object.
    """
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    manual_import = manual_import_class(mock_handler)

    items = [{"path": "/downloads/a.mkv", "seriesId": 1}]
    assert manual_import.update(items) == []

    mock_handler.request.assert_called_once_with("manualimport", method="POST", json_data=items)


@pytest.mark.parametrize("manual_import_class", SYNC_CLASSES)
def test_manual_import_update_rejects_non_list_response(manual_import_class):
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = {"message": "not a list"}
    manual_import = manual_import_class(mock_handler)

    with pytest.raises(ValueError, match="Expected a list response"):
        manual_import.update([])


@pytest.mark.asyncio
@pytest.mark.parametrize("manual_import_class", ASYNC_CLASSES)
async def test_async_manual_import_update_posts_a_list(manual_import_class):
    """Regression test for #165, async client."""
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = []
    manual_import = manual_import_class(mock_handler)

    items = [{"path": "/downloads/a.mkv", "movieId": 1}]
    assert await manual_import.update(items) == []

    mock_handler.request.assert_called_once_with("manualimport", method="POST", json_data=items)


@pytest.mark.asyncio
@pytest.mark.parametrize("manual_import_class", ASYNC_CLASSES)
async def test_async_manual_import_update_rejects_non_list_response(manual_import_class):
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = {"message": "not a list"}
    manual_import = manual_import_class(mock_handler)

    with pytest.raises(ValueError, match="Expected a list response"):
        await manual_import.update([])
