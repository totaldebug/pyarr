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
