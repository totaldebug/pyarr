from datetime import datetime
from unittest.mock import AsyncMock

import pytest

from pyarr._async.common.calendar import Calendar
from pyarr._async.utils.http import RequestHandler


@pytest.mark.asyncio
async def test_calendar_get():
    mock_handler = AsyncMock(spec=RequestHandler)
    calendar = Calendar(mock_handler)

    # Mock successful response
    mock_handler.request.return_value = []

    # Test basic get
    await calendar.get()
    mock_handler.request.assert_called_with("calendar", params={"unmonitored": True})

    # Test with dates
    start = datetime(2024, 1, 1)
    end = datetime(2024, 1, 7)
    await calendar.get(start_date=start, end_date=end)
    mock_handler.request.assert_called_with(
        "calendar", params={"unmonitored": True, "start": "2024-01-01", "end": "2024-01-07"}
    )

    # Test with kwargs
    await calendar.get(includeSeries=True, tags=[1, 2])
    mock_handler.request.assert_called_with(
        "calendar", params={"unmonitored": True, "includeSeries": True, "tags": [1, 2]}
    )
