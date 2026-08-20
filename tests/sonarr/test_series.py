from unittest.mock import AsyncMock, MagicMock

import pytest

from pyarr._async.sonarr.series import Series as AsyncSeries
from pyarr._async.utils.http import RequestHandler as AsyncRequestHandler
from pyarr._sync.sonarr.series import Series
from pyarr._sync.utils.http import RequestHandler


def test_series_delete_single():
    """A single ID deletes via series/{id}, which reads the flags from the query string."""
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    assert series.delete(1, delete_files=True, add_exclusion=True) is True

    mock_handler.request.assert_called_once_with(
        "series/1",
        method="DELETE",
        params={"deleteFiles": True, "addImportListExclusion": True},
    )


def test_series_delete_single_defaults():
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    assert series.delete(1) is True

    mock_handler.request.assert_called_once_with(
        "series/1",
        method="DELETE",
        params={"deleteFiles": False, "addImportListExclusion": False},
    )


def test_series_delete_list_sends_flags_in_body():
    """Regression guard modelled on #190.

    series/editor binds deleteFiles and addImportListExclusion from the request body, so sending
    them as query parameters leaves the series files on disk and skips the list exclusion.
    """
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    assert series.delete([1, 2], delete_files=True, add_exclusion=True) is True

    mock_handler.request.assert_called_once_with(
        "series/editor",
        method="DELETE",
        json_data={"deleteFiles": True, "addImportListExclusion": True, "seriesIds": [1, 2]},
    )
    assert "params" not in mock_handler.request.call_args.kwargs


def test_series_delete_list_defaults():
    mock_handler = MagicMock(spec=RequestHandler)
    series = Series(mock_handler)

    assert series.delete([1]) is True

    mock_handler.request.assert_called_once_with(
        "series/editor",
        method="DELETE",
        json_data={"deleteFiles": False, "addImportListExclusion": False, "seriesIds": [1]},
    )
    assert "params" not in mock_handler.request.call_args.kwargs


def test_series_bulk_update():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = [{"id": 1, "monitored": True}, {"id": 2, "monitored": True}]
    series = Series(mock_handler)

    result = series.bulk_update({"seriesIds": [1, 2], "monitored": True})

    mock_handler.request.assert_called_once_with(
        "series/editor",
        method="PUT",
        json_data={"seriesIds": [1, 2], "monitored": True},
    )
    assert result == [{"id": 1, "monitored": True}, {"id": 2, "monitored": True}]


def test_series_bulk_update_unexpected_response():
    mock_handler = MagicMock(spec=RequestHandler)
    mock_handler.request.return_value = {"message": "nope"}
    series = Series(mock_handler)

    with pytest.raises(ValueError):
        series.bulk_update({"seriesIds": [1], "monitored": True})


@pytest.mark.asyncio
async def test_async_series_delete_single():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    series = AsyncSeries(mock_handler)

    assert await series.delete(1, delete_files=True, add_exclusion=True) is True

    mock_handler.request.assert_called_once_with(
        "series/1",
        method="DELETE",
        params={"deleteFiles": True, "addImportListExclusion": True},
    )


@pytest.mark.asyncio
async def test_async_series_delete_list_sends_flags_in_body():
    """Regression guard modelled on #190, async client."""
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    series = AsyncSeries(mock_handler)

    assert await series.delete([1, 2], delete_files=True, add_exclusion=True) is True

    mock_handler.request.assert_called_once_with(
        "series/editor",
        method="DELETE",
        json_data={"deleteFiles": True, "addImportListExclusion": True, "seriesIds": [1, 2]},
    )
    assert "params" not in mock_handler.request.call_args.kwargs


@pytest.mark.asyncio
async def test_async_series_bulk_update():
    mock_handler = AsyncMock(spec=AsyncRequestHandler)
    mock_handler.request.return_value = [{"id": 1, "monitored": False}]
    series = AsyncSeries(mock_handler)

    result = await series.bulk_update({"seriesIds": [1], "monitored": False})

    mock_handler.request.assert_called_once_with(
        "series/editor",
        method="PUT",
        json_data={"seriesIds": [1], "monitored": False},
    )
    assert result == [{"id": 1, "monitored": False}]
