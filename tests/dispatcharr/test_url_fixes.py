from unittest.mock import AsyncMock

import pytest

from pyarr._async.dispatcharr import Dispatcharr
from pyarr._async.dispatcharr.channel_profiles import ChannelProfiles
from pyarr._async.dispatcharr.hdhr import Hdhr
from pyarr._async.dispatcharr.m3u import M3u
from pyarr._async.dispatcharr.plugins import Plugins
from pyarr._async.dispatcharr.proxy import Proxy
from pyarr._async.utils.http import RequestHandler


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("method", "endpoint"),
    [
        ("get_device_xml", "hdhr/device.xml"),
        ("discover", "hdhr/discover.json"),
        ("get_lineup", "hdhr/lineup.json"),
        ("get_lineup_status", "hdhr/lineup_status.json"),
    ],
)
async def test_hdhr_extension_routes_have_no_trailing_slash(method, endpoint):
    """These four routes are not Django router routes and reject a trailing slash, which
    Dispatcharr answers with its SPA HTML at HTTP 200 rather than a 404."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {}
    hdhr = Hdhr(mock_handler)

    await getattr(hdhr, method)()

    mock_handler.request.assert_called_with(endpoint, params=None)


@pytest.mark.asyncio
async def test_hdhr_devices_keeps_its_trailing_slash():
    """hdhr/devices/ is a router route and does require the slash."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = []
    hdhr = Hdhr(mock_handler)

    await hdhr.get_devices()
    mock_handler.request.assert_called_with("hdhr/devices/", params=None)

    await hdhr.get_devices(item_id=2)
    mock_handler.request.assert_called_with("hdhr/devices/2/", params=None)


@pytest.mark.asyncio
async def test_proxy_routes_escape_the_api_prefix():
    """Dispatcharr serves the proxy views from the server root, not under /api."""
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {}
    proxy = Proxy(mock_handler)

    await proxy.get_ts_status()
    mock_handler.request.assert_called_with("../proxy/ts/status", method="GET")

    await proxy.get_ts_status(channel_id=9)
    mock_handler.request.assert_called_with("../proxy/ts/status/9", method="GET")

    await proxy.stop_ts_stream(9)
    mock_handler.request.assert_called_with("../proxy/ts/stop/9", method="POST")

    await proxy.stop_vod_client()
    mock_handler.request.assert_called_with("../proxy/vod/stop_client/", method="POST")


@pytest.mark.asyncio
async def test_m3u_refresh_account_info_puts_the_profile_id_in_the_path():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {}
    m3u = M3u(mock_handler)

    await m3u.refresh_account_info(5)

    mock_handler.request.assert_called_with("m3u/refresh-account-info/5/", method="POST", json_data=None)


@pytest.mark.asyncio
async def test_channel_profile_partial_update_targets_a_single_channel():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {}
    profiles = ChannelProfiles(mock_handler)

    await profiles.partial_update_channel(3, 77, {"enabled": True})

    mock_handler.request.assert_called_with(
        "channels/profiles/3/channels/77/", method="PATCH", json_data={"enabled": True}
    )


@pytest.mark.asyncio
async def test_plugin_delete_uses_the_action_route():
    """The generic _delete helper produced plugins/plugins//{key}, a double slash."""
    mock_handler = AsyncMock(spec=RequestHandler)
    plugins = Plugins(mock_handler)

    await plugins.delete("my-plugin")

    mock_handler.request.assert_called_with("plugins/plugins/my-plugin/delete/", method="DELETE")


@pytest.mark.asyncio
async def test_plugin_get_detail_has_no_double_slash():
    mock_handler = AsyncMock(spec=RequestHandler)
    mock_handler.request.return_value = {}
    plugins = Plugins(mock_handler)

    await plugins.get("my-plugin")

    endpoint = mock_handler.request.call_args[0][0]
    assert "//" not in endpoint
    assert endpoint == "plugins/plugins/my-plugin/"


def test_dispatcharr_defaults_to_bearer_auth():
    """Dispatcharr rejects a JWT presented in X-Api-Key with 401 Invalid API key."""
    client = Dispatcharr(host="127.0.0.1", api_key="jwt.access.token", tls=False)
    assert client.http_utils.auth_scheme == "bearer"

    client = Dispatcharr(host="127.0.0.1", api_key="generated-api-key", tls=False, auth_scheme="apikey")
    assert client.http_utils.auth_scheme == "apikey"
