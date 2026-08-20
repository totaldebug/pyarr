from unittest.mock import AsyncMock, MagicMock

import pytest

from pyarr._async.common.indexer import Indexer as AsyncCommonIndexer
from pyarr._async.prowlarr.indexer import Indexer as AsyncProwlarrIndexer
from pyarr._async.utils.http import RequestHandler as AsyncRequestHandler
from pyarr._sync.common.indexer import Indexer as CommonIndexer
from pyarr._sync.prowlarr.indexer import Indexer as ProwlarrIndexer
from pyarr._sync.utils.http import RequestHandler

SYNC_CLASSES = [CommonIndexer, ProwlarrIndexer]
ASYNC_CLASSES = [AsyncCommonIndexer, AsyncProwlarrIndexer]

INDEXER = {"id": 1, "name": "Test", "fields": [{"name": "minimumSeeders", "value": 0}]}


@pytest.mark.parametrize("indexer_class", SYNC_CLASSES)
def test_indexer_update_defaults_to_unforced(indexer_class):
    """forceSave is sent as a query parameter and defaults to the API default of false."""
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = INDEXER
    indexer = indexer_class(mock_handler)

    assert indexer.update(1, INDEXER) == INDEXER

    mock_handler.request.assert_called_once_with(
        "indexer/1", method="PUT", json_data=INDEXER, params={"forceSave": False}
    )


@pytest.mark.parametrize("indexer_class", SYNC_CLASSES)
def test_indexer_update_can_force_save(indexer_class):
    """Regression test for #169.

    Some configurations, such as a minimum seeders of 0, raise a validation warning that the
    API refuses to save unless forceSave=true is passed.
    """
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = INDEXER
    indexer = indexer_class(mock_handler)

    assert indexer.update(1, INDEXER, force_save=True) == INDEXER

    mock_handler.request.assert_called_once_with(
        "indexer/1", method="PUT", json_data=INDEXER, params={"forceSave": True}
    )


@pytest.mark.parametrize("indexer_class", SYNC_CLASSES)
def test_indexer_update_rejects_non_dict_response(indexer_class):
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    indexer = indexer_class(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        indexer.update(1, INDEXER)


@pytest.mark.asyncio
@pytest.mark.parametrize("indexer_class", ASYNC_CLASSES)
async def test_async_indexer_update_defaults_to_unforced(indexer_class):
    """forceSave is sent as a query parameter and defaults to the API default of false."""
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = INDEXER
    indexer = indexer_class(mock_handler)

    assert await indexer.update(1, INDEXER) == INDEXER

    mock_handler.request.assert_called_once_with(
        "indexer/1", method="PUT", json_data=INDEXER, params={"forceSave": False}
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("indexer_class", ASYNC_CLASSES)
async def test_async_indexer_update_can_force_save(indexer_class):
    """Regression test for #169, async client."""
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = INDEXER
    indexer = indexer_class(mock_handler)

    assert await indexer.update(1, INDEXER, force_save=True) == INDEXER

    mock_handler.request.assert_called_once_with(
        "indexer/1", method="PUT", json_data=INDEXER, params={"forceSave": True}
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("indexer_class", ASYNC_CLASSES)
async def test_async_indexer_update_rejects_non_dict_response(indexer_class):
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = []
    indexer = indexer_class(mock_handler)

    with pytest.raises(ValueError, match="Expected a dictionary response"):
        await indexer.update(1, INDEXER)
