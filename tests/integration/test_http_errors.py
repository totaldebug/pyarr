import pytest

from pyarr.exceptions import (
    PyarrBadRequest,
    PyarrMethodNotAllowed,
    PyarrResourceNotFound,
    PyarrUnauthorizedError,
)
from pyarr.sonarr import Sonarr


def test_http_unauthorized():
    # Use a wrong API key and provide api_ver to avoid auto-detection failure in __init__
    client = Sonarr(host="localhost", api_key="wrong_key", port=8989, tls=False, api_ver="v3")
    with pytest.raises(PyarrUnauthorizedError):
        client.system.get_status()


def test_http_not_found(sonarr_client):
    with pytest.raises(PyarrResourceNotFound):
        # Use a non-existent endpoint
        sonarr_client.http_utils.request("non_existent_endpoint")


def test_http_method_not_allowed(sonarr_client):
    with pytest.raises(PyarrMethodNotAllowed):
        # Use POST on an endpoint that only supports GET
        sonarr_client.http_utils.request("system/status", method="POST")


def test_http_bad_request(sonarr_client):
    # Try to trigger 400 by sending invalid data type
    with pytest.raises(PyarrBadRequest):
        sonarr_client.http_utils.request("tag", method="POST", json_data={"label": "test", "id": "not_an_int"})


def test_http_no_api_key():
    with pytest.raises(ValueError, match="No API Key provided"):
        Sonarr(host="localhost", api_key="", port=8989, tls=False)
