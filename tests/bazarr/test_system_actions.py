from unittest.mock import AsyncMock

import httpx
import pytest

from pyarr._async.bazarr.system import BazarrSystem
from pyarr._async.utils.http import RequestHandler
from pyarr.exceptions import PyarrConnectionError


def _dropped(cause: Exception) -> PyarrConnectionError:
    """Builds the error the request handler raises when a connection fails mid-flight."""
    error = PyarrConnectionError("Error occurred while communicating with your instance.")
    error.__cause__ = cause
    return error


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ["restart", "shutdown"])
@pytest.mark.parametrize(
    "cause",
    [
        httpx.RemoteProtocolError("Server disconnected"),
        httpx.ReadError("Connection reset by peer"),
    ],
)
async def test_dropped_connection_is_expected(action, cause):
    """Bazarr closes the connection instead of answering, so this must not raise."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.side_effect = _dropped(cause)
    system = BazarrSystem(mock_handler)

    assert await getattr(system, f"request_{action}")() is None

    mock_handler.request.assert_called_once_with("system", method="POST", params={"action": action})


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ["restart", "shutdown"])
async def test_unreachable_instance_still_raises(action):
    """A ConnectError means Bazarr was never reached, which the caller must hear about."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.side_effect = _dropped(httpx.ConnectError("All connection attempts failed"))
    system = BazarrSystem(mock_handler)

    with pytest.raises(PyarrConnectionError):
        await getattr(system, f"request_{action}")()


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ["restart", "shutdown"])
async def test_unrelated_errors_are_not_swallowed(action):
    """Only a dropped connection is expected; nothing else should be hidden."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.side_effect = ValueError("something else went wrong")
    system = BazarrSystem(mock_handler)

    with pytest.raises(ValueError):
        await getattr(system, f"request_{action}")()


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ["restart", "shutdown"])
async def test_a_normal_response_is_also_fine(action):
    """If a future Bazarr answers before closing, that must not become an error either."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = None
    system = BazarrSystem(mock_handler)

    assert await getattr(system, f"request_{action}")() is None
