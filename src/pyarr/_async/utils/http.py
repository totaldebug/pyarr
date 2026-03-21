from __future__ import annotations

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

        Raises:
            ValueError: If no API Key is provided or if unable to retrieve API version automatically.
        """
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
        # Set default timeout to None to match requests behavior if not specified
        # Enable follow_redirects to match requests behavior
        self.session: httpx.AsyncClient | None = httpx.AsyncClient(timeout=request_timeout, follow_redirects=True)
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
        if self.session:
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
        headers = headers or {}
        headers["X-Api-Key"] = self.api_key

        if self.session is None:
            self.session = httpx.AsyncClient(timeout=self.request_timeout, follow_redirects=True)

        try:
            response = await self.session.request(
                method,
                str(url),
                data=data,
                json=json_data,
                params=params,
                headers=headers,
            )
        except httpx.TimeoutException as exception:
            msg = "Timeout occurred while connecting to your instance."
            raise PyarrConnectionError(msg) from exception
        except httpx.RequestError as exception:
            msg = "Error occurred while communicating with your instance."
            raise PyarrConnectionError(msg) from exception

        if response.status_code // 100 in [4, 5]:
            self._handle_error(response)

        content_type = response.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return response.json()

        text = response.text
        return {"message": text}

    def _handle_error(self, response: httpx.Response) -> None:
        """Handles error responses by raising appropriate exceptions.

        Args:
            response (httpx.Response): The error response.

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
        status_code = response.status_code
        try:
            error_data = response.json()
            message = error_data.get("message", response.text)
        except Exception:
            message = response.text

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
