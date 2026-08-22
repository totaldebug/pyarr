"""Request-shape coverage for the Servarr restart and shutdown calls.

The live equivalents in tests/<app>/test_system.py are marked ``destructive`` and
deselected by default, because restarting the application under test leaves it unavailable
for several seconds and sometimes kills it outright. These assert the same thing without
touching a running instance.
"""

from unittest.mock import AsyncMock

import pytest

from pyarr._async.common.system import MediaSystem, System
from pyarr._async.utils.http import RequestHandler


@pytest.mark.asyncio
@pytest.mark.parametrize("system_class", [System, MediaSystem])
@pytest.mark.parametrize(
    ("method", "endpoint"),
    [
        ("request_restart", "system/restart"),
        ("request_shutdown", "system/shutdown"),
    ],
)
async def test_servarr_restart_and_shutdown_post_to_their_own_endpoints(system_class, method, endpoint):
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"restarting": True}
    system = system_class(mock_handler)

    response = await getattr(system, method)()

    assert response == {"restarting": True}
    mock_handler.request.assert_called_once_with(endpoint, method="POST")


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ["request_restart", "request_shutdown"])
async def test_servarr_actions_reject_a_non_dict_response(method):
    """A list response means the path was wrong, so it must not be passed off as a result."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    system = System(mock_handler)

    with pytest.raises(ValueError):
        await getattr(system, method)()
