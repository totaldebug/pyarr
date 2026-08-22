from unittest.mock import AsyncMock

import pytest

from pyarr._async.bazarr import Bazarr
from pyarr._async.bazarr.system import BazarrSystem
from pyarr._async.common.system import System
from pyarr._async.utils.http import RequestHandler


@pytest.mark.asyncio
async def test_bazarr_system_uses_bazarr_paths():
    """Bazarr spells health and tasks differently to the Servarr applications."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {"data": {}}
    system = BazarrSystem(mock_handler)

    await system.get_status()
    mock_handler.request.assert_called_with("system/status", params=None)

    await system.get_health()
    mock_handler.request.assert_called_with("system/health", params=None)

    await system.get_tasks()
    mock_handler.request.assert_called_with("system/tasks", params=None)

    await system.get_tasks("update_series")
    mock_handler.request.assert_called_with("system/tasks", params={"taskid": "update_series"})


@pytest.mark.asyncio
async def test_bazarr_system_run_task():
    mock_handler = AsyncMock(spec=RequestHandler)
    system = BazarrSystem(mock_handler)

    await system.run_task("update_series")

    mock_handler.request.assert_called_with("system/tasks", method="POST", params={"taskid": "update_series"})


@pytest.mark.asyncio
async def test_bazarr_restart_and_shutdown_use_the_action_parameter():
    """Bazarr has no system/restart or system/shutdown route, only POST system."""
    mock_handler = AsyncMock(spec=RequestHandler)
    system = BazarrSystem(mock_handler)

    await system.request_restart()
    mock_handler.request.assert_called_with("system", method="POST", params={"action": "restart"})

    await system.request_shutdown()
    mock_handler.request.assert_called_with("system", method="POST", params={"action": "shutdown"})


def test_bazarr_client_replaces_the_servarr_system_component():
    """The inherited Servarr System silently returned Bazarr's SPA HTML, so it must be gone."""
    client = Bazarr(host="127.0.0.1", api_key="123456789abcdefg123456789", tls=False, api_ver="")

    assert isinstance(client.system, BazarrSystem)
    assert not isinstance(client.system, System)

    # Endpoints Bazarr does not serve at all must not be reachable on the client.
    for absent in ("get_diskspace", "get_routes", "get_routes_duplicate", "get_task"):
        assert not hasattr(client.system, absent), f"Bazarr should not expose system.{absent}"
