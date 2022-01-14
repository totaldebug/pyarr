from typing import Any

import requests
from requests import Response
from requests.auth import HTTPBasicAuth

from .exceptions import (
    PyarrAccessRestricted,
    PyarrBadGateway,
    PyarrConnectionError,
    PyarrResourceNotFound,
    PyarrUnauthorizedError,
)


class RequestHandler:
    """Base class for API Wrappers"""

    def __init__(
        self,
        host_url: str,
        api_key: str,
    ):
        """Constructor for connection to Arr API

        Args:
            host_url (str): Host URL to Arr api
            api_key (str): API Key for Arr api
        """
        self.host_url = host_url
        self.api_key = api_key
        self.session = requests.Session()
        self.auth = None

    def _request_url(self, path: str, ver_uri: str) -> str:
        """Builds the URL for the request to use.

        Args:
            path (str): Destination for specific call
            ver_uri (str): API Version number

        Returns:
            str: string URL for API endpoint
        """
        return f"{self.host_url}/api{ver_uri}/{path}"

    def basic_auth(self, username: str, password: str) -> HTTPBasicAuth:
        """If you have basic authentication setup you will need to pass your
        username and passwords to the requests.auth.HTTPBASICAUTH() method.

        Args:
            username (str): Username for basic auth.
            password (str): Password for basic auth.

        Returns:
            Object: HTTP Auth object
        """
        return HTTPBasicAuth(username, password)

    def request_get(
        self, path: str, ver_uri: str = "", params: dict = None
    ) -> list[dict] | dict | Response:
        """Wrapper on any get requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        try:
            res = self.session.get(
                self._request_url(path, ver_uri),
                headers=headers,
                params=params,
                auth=self.auth,
            )
        except requests.Timeout as exception:
            raise PyarrConnectionError(
                "Timeout occurred while connecting to API"
            ) from exception
        return self._process_response(res)

    def request_post(
        self, path, ver_uri="", params=None, data=None
    ) -> list[dict] | dict | Response:
        """Wrapper on any post requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.
            data (dict, optional): Payload to send with request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        try:
            res = self.session.post(
                self._request_url(path, ver_uri),
                headers=headers,
                params=params,
                json=data,
                auth=self.auth,
            )
        except requests.Timeout as exception:
            raise PyarrConnectionError(
                "Timeout occurred while connecting to API"
            ) from exception
        return self._process_response(res)

    def request_put(
        self, path, ver_uri="", params=None, data=None
    ) -> list[dict] | dict | Response:
        """Wrapper on any put requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.
            data (dict, optional): Payload to send with request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        try:
            res = self.session.put(
                self._request_url(path, ver_uri),
                headers=headers,
                params=params,
                json=data,
                auth=self.auth,
            )
        except requests.Timeout as exception:
            raise PyarrConnectionError(
                "Timeout occurred while connecting to API"
            ) from exception
        return self._process_response(res)

    def request_del(
        self, path, ver_uri="", params=None, data=None
    ) -> list[dict] | dict | Response:
        """Wrapper on any delete requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.
            data (dict, optional): Payload to send with request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        try:
            res = self.session.delete(
                self._request_url(path, ver_uri),
                headers=headers,
                params=params,
                json=data,
                auth=self.auth,
            )
        except requests.Timeout as exception:
            raise PyarrConnectionError(
                "Timeout occurred while connecting to API"
            ) from exception
        return self._process_response(res)

    def _process_response(self, res) -> list[dict] | Response | Any:
        """Check the response status code and error or return results

        Args:
            res (str): JSON or Text response from API Call

        Raises:
            PyarrUnauthorizedError: Invalid API Key
            PyarrAccessRestricted: Invalid Permissions
            PyarrResourceNotFound: Incorrect Resource
            PyarrBadGateway: Bad Gateway

        Returns:
            JSON: Array
        """
        if res.status_code == 401:
            raise PyarrUnauthorizedError(
                "Unauthorized. Please ensure valid API Key is used.", {}
            )
        if res.status_code == 403:
            raise PyarrAccessRestricted(
                "Access restricted. Please ensure API Key has correct permissions", {}
            )
        if res.status_code == 404:
            raise PyarrResourceNotFound("Resource not found")
        if res.status_code == 502:
            raise PyarrBadGateway("Bad Gateway. Check your server is accessible")
        content_type = res.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return res.json()
        return res
