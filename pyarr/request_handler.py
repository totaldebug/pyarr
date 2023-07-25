from typing import Any, Optional, Type, Union

import aiohttp
import requests
from aiohttp.client import _RequestContextManager
from aiohttp.web_exceptions import HTTPRequestTimeout
from requests import Response
from requests.auth import HTTPBasicAuth

from .exceptions import (
    PyarrAccessRestricted,
    PyarrBadGateway,
    PyarrBadRequest,
    PyarrConnectionError,
    PyarrMethodNotAllowed,
    PyarrResourceNotFound,
    PyarrServerError,
    PyarrUnauthorizedError,
)
from .types import _ReturnType

AIOHTTP_SESSION = aiohttp.ClientSession()


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
        self.host_url = host_url.rstrip("/")
        self.api_key = api_key
        self.session: requests.Session = requests.Session()
        self.auth: Union[HTTPBasicAuth, None] = None

    def _request_url(self, path: str, ver_uri: str) -> str:
        """Builds the URL for the request to use.

        Args:
            path (str): Destination for specific call
            ver_uri (str): API Version number

        Returns:
            str: string URL for API endpoint
        """
        return f"{self.host_url}/api{ver_uri}/{path}"

    def basic_auth(self, username: str, password: str) -> Union[HTTPBasicAuth, None]:
        """If you have basic authentication setup you will need to pass your
        username and passwords to the HTTPBASICAUTH() method.

        Args:
            username (str): Username for basic auth.
            password (str): Password for basic auth.

        Returns:
            Object: HTTP Auth object
        """
        return HTTPBasicAuth(username, password)

    def _get(
        self,
        path: str,
        ver_uri: str = "",
        params: Union[dict[str, Any], list[tuple[str, Any]], None] = None,
    ) -> _ReturnType:
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
                "Timeout occurred while connecting to API."
            ) from exception
        response = _process_response(res)
        return self._check_type(res, dict if isinstance(response, dict) else list)

    def _post(
        self,
        path: str,
        ver_uri: str = "",
        params: Union[dict, None] = None,
        data: Union[list[dict], dict, None] = None,
    ) -> _ReturnType:
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
                "Timeout occurred while connecting to API."
            ) from exception
        response = _process_response(res)
        return self._check_type(res, dict if isinstance(response, dict) else list)

    def _put(
        self,
        path: str,
        ver_uri: str,
        params: Optional[dict] = None,
        data: Optional[Union[dict[str, Any], list[dict[str, Any]]]] = None,
    ) -> _ReturnType:
        """Wrapper on any put requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            ver_uri (str): API Version
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
                "Timeout occurred while connecting to API."
            ) from exception

        response = _process_response(res)
        return self._check_type(res, dict if isinstance(response, dict) else list)

    def _delete(
        self,
        path: str,
        ver_uri: str = "",
        params: Union[dict, None] = None,
        data: Union[dict, None] = None,
    ) -> Union[Response, dict[str, Any], dict[Any, Any]]:
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
        response = _process_response(res)
        if isinstance(response, dict):
            assert isinstance(response, dict)
        else:
            assert isinstance(response, Response)
        return response

    def _check_type(self, value: Any, *types: Type) -> Any:
        """Takes the response and asserts its type

        Args:
            value (Any): Response from request
            types (Type): The types that should be checked for

        Returns:
            Any: Many possible return types
        """
        assert isinstance(value, types)
        return value


class AsyncRequestHandler:
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
        self.host_url = host_url.rstrip("/")
        self.api_key = api_key
        self.session = AIOHTTP_SESSION
        self.auth: Union[aiohttp.BasicAuth, None] = None

    def _request_url(self, path: str, ver_uri: str) -> str:
        """Builds the URL for the request to use.

        Args:
            path (str): Destination for specific call
            ver_uri (str): API Version number

        Returns:
            str: string URL for API endpoint
        """
        return f"{self.host_url}/api{ver_uri}/{path}"

    def basic_auth(
        self, username: str, password: str
    ) -> Union[aiohttp.BasicAuth, None]:
        """If you have basic authentication setup you will need to pass your
        username and passwords to the HTTPBASICAUTH() method.

        Args:
            username (str): Username for basic auth.
            password (str): Password for basic auth.

        Returns:
            Object: HTTP Auth object
        """
        return aiohttp.BasicAuth(username, password)

    async def _get(
        self,
        path: str,
        ver_uri: str = "",
        params: Union[dict[str, Any], list[tuple[str, Any]], None] = None,
    ) -> _ReturnType:
        """Wrapper on any get requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        response = await _aprocess_response(
            self.session.get(
                self._request_url(path, ver_uri),
                headers=headers,
                params=params,
                auth=self.auth,
            )
        )
        return self._check_type(response, dict, list)

    async def _post(
        self,
        path: str,
        ver_uri: str = "",
        params: Union[dict, None] = None,
        data: Union[list[dict], dict, None] = None,
    ) -> _ReturnType:
        """Wrapper on any post requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.
            data (dict, optional): Payload to send with request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        response = await _aprocess_response(
            self.session.post(
                self._request_url(path, ver_uri),
                headers=headers,
                params=params,
                json=data,
                auth=self.auth,
            )
        )
        return self._check_type(response, dict, list)

    async def _put(
        self,
        path: str,
        ver_uri: str,
        params: Optional[dict] = None,
        data: Optional[Union[dict[str, Any], list[dict[str, Any]]]] = None,
    ) -> _ReturnType:
        """Wrapper on any put requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            ver_uri (str): API Version
            params (dict, optional): URL Parameters to send with the request. Defaults to None.
            data (dict, optional): Payload to send with request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        response = await _aprocess_response(
            self.session.put(
                self._request_url(path, ver_uri),
                headers=headers,
                params=params,
                json=data,
                auth=self.auth,
            )
        )
        return self._check_type(response, dict, list)

    async def _delete(
        self,
        path: str,
        ver_uri: str = "",
        params: Union[dict, None] = None,
        data: Union[dict, None] = None,
    ) -> Union[aiohttp.ClientResponse, dict[str, Any], dict[Any, Any]]:
        """Wrapper on any delete requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.
            data (dict, optional): Payload to send with request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        response = await _aprocess_response(
            self.session.delete(
                self._request_url(path, ver_uri),
                headers=headers,
                params=params,
                json=data,
                auth=self.auth,
            )
        )
        return self._check_type(response, dict, aiohttp.ClientResponse)

    def _check_type(self, value: Any, *types: Type) -> Any:
        """Takes the response and asserts its type

        Args:
            value (Any): Response from request
            types (Type): The types that should be checked for

        Returns:
            Any: Many possible return types
        """
        assert isinstance(value, types)
        return value


def _process_response(
    res: Response,
) -> Union[list[dict[str, Any]], Response, dict[str, Any], Any]:
    """Check the response status code and error or return results

    Args:
        res (str): JSON or Text response from API Call

    Raises:
        TODO: Document the exceptions raised by this function
        PyarrUnauthorizedError: Invalid API Key
        PyarrAccessRestricted: Invalid Permissions
        PyarrResourceNotFound: Incorrect Resource
        PyarrBadGateway: Bad Gateway

    Returns:
        JSON: Array
    """
    if res.status_code == 400:
        raise PyarrBadRequest(f"Bad Request, possibly a bug. {str(res.content)}")

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
    if res.status_code == 405:
        raise PyarrMethodNotAllowed(f"The endpoint {res.url} is not allowed")
    if res.status_code == 500:
        raise PyarrServerError(
            f"Internal Server Error: {res.json()['message']}",
            res.json(),
        )
    if res.status_code == 502:
        raise PyarrBadGateway("Bad Gateway. Check your server is accessible.")

    content_type = res.headers.get("Content-Type", "")
    if "application/json" in content_type:
        return res.json()
    else:
        assert isinstance(res, Response)
    return res


async def _aprocess_response(request: _RequestContextManager):
    """Check the response status code and error or return results

    Args:
        res (str): JSON or Text response from API Call

    Raises:
        TODO: Document the exceptions raised by this function
        PyarrUnauthorizedError: Invalid API Key
        PyarrAccessRestricted: Invalid Permissions
        PyarrResourceNotFound: Incorrect Resource
        PyarrBadGateway: Bad Gateway

    Returns:
        JSON: Array
    """
    try:
        async with request as res:
            if res.status == 400:
                raise PyarrBadRequest(
                    f"Bad Request, possibly a bug. {str(res.content)}"
                )

            if res.status == 401:
                raise PyarrUnauthorizedError(
                    "Unauthorized. Please ensure valid API Key is used.", {}
                )
            if res.status == 403:
                raise PyarrAccessRestricted(
                    "Access restricted. Please ensure API Key has correct permissions",
                    {},
                )
            if res.status == 404:
                raise PyarrResourceNotFound("Resource not found")
            if res.status == 405:
                raise PyarrMethodNotAllowed(f"The endpoint {res.url} is not allowed")
            if res.status == 500:
                res_json = await res.json()
                raise PyarrServerError(
                    f"Internal Server Error: {res_json['message']}",
                    res_json,
                )
            if res.status == 502:
                raise PyarrBadGateway("Bad Gateway. Check your server is accessible.")

            content_type = res.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return await res.json()

            assert isinstance(res, aiohttp.ClientResponse)
            return res

    except HTTPRequestTimeout as exception:
        raise PyarrConnectionError(
            "Timeout occurred while connecting to API"
        ) from exception
