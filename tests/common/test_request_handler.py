import json

import httpx
import pytest

from pyarr._async.utils.http import RequestHandler as AsyncRequestHandler
from pyarr._sync.utils.http import RequestHandler


def _transport(captured):
    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["content"] = request.content
        return httpx.Response(200, json=[], headers={"Content-Type": "application/json"})

    return handler


def test_request_sends_list_json_data():
    """A list json_data must reach the wire as a JSON array, not be coerced to an object."""
    captured: dict[str, object] = {}
    session = httpx.Client(transport=httpx.MockTransport(_transport(captured)))
    handler = RequestHandler(host="localhost", api_key="key", port=8989, tls=False, api_ver="v3", session=session)

    payload = [{"path": "/downloads/a.mkv", "seriesId": 1}]
    assert handler.request("manualimport", method="POST", json_data=payload) == []

    assert captured["method"] == "POST"
    assert json.loads(captured["content"]) == payload


@pytest.mark.asyncio
async def test_async_request_sends_list_json_data():
    captured: dict[str, object] = {}
    session = httpx.AsyncClient(transport=httpx.MockTransport(_transport(captured)))
    handler = AsyncRequestHandler(host="localhost", api_key="key", port=8989, tls=False, api_ver="v3", session=session)

    payload = [{"path": "/downloads/a.mkv", "movieId": 1}]
    assert await handler.request("manualimport", method="POST", json_data=payload) == []

    assert captured["method"] == "POST"
    assert json.loads(captured["content"]) == payload


def _no_content_transport(captured):
    def handler(request: httpx.Request) -> httpx.Response:
        captured["method"] = request.method
        captured["url"] = str(request.url)
        # Bazarr answers a successful action with a 204 that has no body but still claims JSON.
        return httpx.Response(204, headers={"Content-Type": "application/json"})

    return handler


def test_request_returns_none_for_204_no_content():
    """A 204 has no body to decode, even when the server advertises a JSON content type."""
    captured: dict[str, object] = {}
    session = httpx.Client(transport=httpx.MockTransport(_no_content_transport(captured)))
    handler = RequestHandler(host="localhost", api_key="key", port=6767, tls=False, api_ver="", session=session)

    assert handler.request("series", method="PATCH", params={"action": "sync", "seriesid": 1}) is None

    assert captured["method"] == "PATCH"


@pytest.mark.asyncio
async def test_async_request_returns_none_for_204_no_content():
    captured: dict[str, object] = {}
    session = httpx.AsyncClient(transport=httpx.MockTransport(_no_content_transport(captured)))
    handler = AsyncRequestHandler(host="localhost", api_key="key", port=6767, tls=False, api_ver="", session=session)

    assert await handler.request("series", method="PATCH", params={"action": "sync", "seriesid": 1}) is None

    assert captured["method"] == "PATCH"
