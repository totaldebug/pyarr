import httpx
import pytest

from pyarr._async.utils.http import RequestHandler


def _handler(**kwargs):
    return RequestHandler("127.0.0.1", "the-token", port=1234, tls=False, api_ver="v3", **kwargs)


def test_default_scheme_is_apikey():
    assert _handler().auth_scheme == "apikey"


def test_unknown_scheme_is_rejected():
    with pytest.raises(ValueError, match="Unknown auth scheme"):
        _handler(auth_scheme="basic")


@pytest.mark.parametrize(
    ("scheme", "expected_header", "expected_value"),
    [
        ("apikey", "X-Api-Key", "the-token"),
        ("bearer", "Authorization", "Bearer the-token"),
    ],
)
@pytest.mark.asyncio
async def test_credential_is_presented_in_the_right_header(scheme, expected_header, expected_value, monkeypatch):
    captured = {}

    async def fake_request(self, method, url, **kwargs):
        captured["headers"] = kwargs.get("headers", {})
        return httpx.Response(200, json={}, headers={"Content-Type": "application/json"})

    monkeypatch.setattr(httpx.AsyncClient, "request", fake_request)

    handler = _handler(auth_scheme=scheme)
    await handler.request("system/status")

    assert captured["headers"][expected_header] == expected_value
    other = "Authorization" if expected_header == "X-Api-Key" else "X-Api-Key"
    assert other not in captured["headers"]
