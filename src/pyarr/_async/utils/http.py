from __future__ import annotations

import inspect
from collections.abc import Mapping
from typing import Any

import backoff
import httpx
from yarl import URL

from pyarr.exceptions import (
    PyarrAccessRestricted,
    PyarrBadGateway,
    PyarrBadRequest,
    PyarrConnectionError,
    PyarrMethodNotAllowed,
    PyarrResourceNotFound,
    PyarrServerError,
    PyarrUnauthorizedError,
)


class RequestHandler:
    """HTTP request handler for Arr APIs."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int | None = None,
        tls: bool = True,
        base_path: str = "",
        request_timeout: int | None = None,
        api_ver: str | None = None,
        session: httpx.AsyncClient | None = None,
        verify_ssl: bool = True,
        headers: dict[str, str] | None = None,
    ) -> None:
        """
        Initializes the HTTP client with the provided host, API key, and optional parameters.

        Args:
            host (str): The host to connect to.
            api_key (str): The API key for authentication.
            port (int | None, optional): The port to connect to. Defaults to None.
            tls (bool, optional): Whether to use TLS. Defaults to True.
            base_path (str, optional): The base path for the API. Defaults to "".
            request_timeout (int | None, optional): The timeout for requests. Defaults to None.
            api_ver (str | None, optional): The API version to use, this is auto detected. Defaults to None.
            session (httpx.AsyncClient | None, optional): An existing httpx.AsyncClient session. Defaults to None.
            verify_ssl (bool, optional): Whether to verify SSL certificates. Defaults to True.
            headers (dict[str, str] | None, optional): Default headers to include in requests. Defaults to None.

        Raises:
            ValueError: If no API Key is provided or if unable to retrieve API version automatically.
        """
        if "://" in host:
            url = URL(host)
            scheme = url.scheme
            host = url.host or host
            port = url.port or port
            if url.path and url.path != "/":
                base_path = str(url.path).rstrip("/") + "/" + base_path.lstrip("/")
        else:
            scheme = "https" if tls else "http"

        self.base_url = URL.build(
            scheme=scheme,
            host=host,
            port=port,
            path=base_path,
        )

        if not api_key:
            raise ValueError("No API Key provided")

        self.api_key = api_key  # Initialize api_key before making requests
        self.request_timeout = request_timeout
        self.verify_ssl = verify_ssl
        self.headers = headers or {}
        # Set default timeout to None to match requests behavior if not specified
        # Enable follow_redirects to match requests behavior
        if session:
            self.session: httpx.AsyncClient | None = session
            self._owns_session = False
        else:
            self.session = httpx.AsyncClient(
                timeout=request_timeout,
                follow_redirects=True,
                verify=verify_ssl,
            )
            self._owns_session = True
        self._api_ver = api_ver
        self.api_url: URL | None = None
        if api_ver:
            self.api_url = self.base_url.joinpath("api").joinpath(api_ver)

    async def __aenter__(self) -> RequestHandler:
        """Enter the runtime context related to this object.

        Returns:
            RequestHandler: The request handler instance.
        """
        return self

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        """Exit the runtime context related to this object.

        Args:
            exc_type (Any): The exception type.
            exc_value (Any): The exception value.
            traceback (Any): The traceback.
        """
        if self.session and self._owns_session:
            await self.session.aclose()
            self.session = None

    async def _get_api_version(self) -> str:
        """Retrieves the API version from the server.

        Returns:
            str: The API version.

        Raises:
            PyarrConnectionError: If unable to retrieve the API version.
        """
        try:
            # Call request directly with the "api" endpoint
            # This will skip the version check in request()
            response = await self.request("api")
            if isinstance(response, dict) and "current" in response:
                return response["current"]
            else:
                raise ValueError("Unexpected response format or 'current' key not found")
        except Exception as e:
            raise PyarrConnectionError(
                f"Unable to retrieve API Version automatically, please specify it in the initialization: {e}"
            ) from e

    @backoff.on_exception(backoff.expo, (httpx.RequestError, httpx.TimeoutException), max_tries=5, logger=None)
    async def request(
        self,
        endpoint: str,
        method: str = "GET",
        data: Any = None,
        json_data: dict[str, Any] | None = None,
        params: Mapping[str, Any] | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Sends a request to the specified endpoint using the provided method and data.

        Args:
            endpoint (str): The endpoint to send the request to.
            method (str, optional): The HTTP method to use. Defaults to "GET".
            data (Any, optional): The data to send in the request body. Defaults to None.
            json_data (dict[str, Any] | None, optional): The JSON data to send in the request body. Defaults to None.
            params (Mapping[str, Any] | None, optional): The parameters to include in the request URL. Defaults to None.
            headers (Optional[dict], optional): The headers to include in the request. Defaults to None.

        Raises:
            PyarrConnectionError: If a timeout or error occurs during the request.
            PyarrBadRequest: 400 Bad Request.
            PyarrUnauthorizedError: 401 Unauthorized.
            PyarrAccessRestricted: 403 Forbidden.
            PyarrResourceNotFound: 404 Not Found.
            PyarrMethodNotAllowed: 405 Method Not Allowed.
            PyarrServerError: 500 Internal Server Error.
            PyarrBadGateway: 502 Bad Gateway.
            Exception: If the response status code indicates an error.

        Returns:
            Any: The response data as a dictionary, list, or httpx.Response object.
        """
        if endpoint == "api":
            url = self.base_url.joinpath(endpoint)
        else:
            if self.api_url is None:
                if self._api_ver is None:
                    self._api_ver = await self._get_api_version()
                self.api_url = self.base_url.joinpath("api").joinpath(self._api_ver)
            url = self.api_url.joinpath(endpoint)

        if params:
            # Create a mutable copy of params if it's not already one
            params_copy = dict(params)
            for key, value in params_copy.items():
                if isinstance(value, bool):
                    params_copy[key] = str(value).lower()
            params = params_copy

        # Merge default headers with request-specific headers
        request_headers = self.headers.copy()
        if headers:
            request_headers.update(headers)
        request_headers["X-Api-Key"] = self.api_key

        if self.session is None:
            self.session = httpx.AsyncClient(
                timeout=self.request_timeout,
                follow_redirects=True,
                verify=self.verify_ssl,
            )
            self._owns_session = True

        try:
            response = await self.session.request(
                method,
                str(url),
                data=data,
                json=json_data,
                params=params,
                headers=request_headers,
            )
        except httpx.TimeoutException as exception:
            msg = "Timeout occurred while connecting to your instance."
            raise PyarrConnectionError(msg) from exception
        except httpx.RequestError as exception:
            msg = "Error occurred while communicating with your instance."
            raise PyarrConnectionError(msg) from exception

        # Handle both httpx (.status_code) and aiohttp (.status)
        status_code = int(getattr(response, "status", getattr(response, "status_code", 0)))

        if status_code // 100 in [4, 5]:
            await self._handle_error(response)

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            res_json = response.json()
            if inspect.isawaitable(res_json):
                return await res_json
            return res_json

        res_text = getattr(response, "text", "")
        if callable(res_text):
            res_text = res_text()
        if inspect.isawaitable(res_text):
            res_text = await res_text

        return {"message": res_text}

    async def _handle_error(self, response: Any) -> None:
        """Handles error responses by raising appropriate exceptions.

        Args:
            response (Any): The error response (httpx.Response or aiohttp.ClientResponse).

        Raises:
            PyarrBadRequest: 400 Bad Request.
            PyarrUnauthorizedError: 401 Unauthorized.
            PyarrAccessRestricted: 403 Forbidden.
            PyarrResourceNotFound: 404 Not Found.
            PyarrMethodNotAllowed: 405 Method Not Allowed.
            PyarrServerError: 500 Internal Server Error.
            PyarrBadGateway: 502 Bad Gateway.
            Exception: For other 4xx/5xx errors.
        """
        status_code = int(getattr(response, "status", getattr(response, "status_code", 0)))
        try:
            res_json = response.json()
            if inspect.isawaitable(res_json):
                error_data = await res_json
            else:
                error_data = res_json

            res_text = getattr(response, "text", "")
            if callable(res_text):
                res_text = res_text()
            if inspect.isawaitable(res_text):
                res_text = await res_text

            if isinstance(error_data, dict):
                message = error_data.get("message", res_text)
            else:
                message = res_text
        except Exception:
            res_text = getattr(response, "text", "")
            if callable(res_text):
                res_text = res_text()
            if inspect.isawaitable(res_text):
                res_text = await res_text
            message = res_text

        if status_code == 400:
            raise PyarrBadRequest(message)
        if status_code == 401:
            raise PyarrUnauthorizedError(message)
        if status_code == 403:
            raise PyarrAccessRestricted(message)
        if status_code == 404:
            raise PyarrResourceNotFound(message)
        if status_code == 405:
            raise PyarrMethodNotAllowed(message)
        if status_code == 500:
            raise PyarrServerError(message, response)
        if status_code == 502:
            raise PyarrBadGateway(message)

        raise Exception(status_code, message)
