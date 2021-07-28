import requests


class RequestAPI:
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

    def basic_auth(self, username, password):
        """If you have basic authentication setup you will need to pass your
        username and passwords to the requests.auth.HTTPBASICAUTH() method.

        Args:
            username (str): Username for basic auth.
            password (str): Password for basic auth.

        Returns:
            Object: HTTP Auth object
        """
        self.auth = requests.auth.HTTPBasicAuth(username, password)
        return self.auth

    def request_get(self, path, params=None):
        """Wrapper on any get requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.get(
            request_url, headers=headers, params=params, auth=self.auth
        )
        return res.json()

    def request_post(self, path, params=None, data=None):
        """Wrapper on any post requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.
            data (dict, optional): Payload to send with request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.post(
            request_url, headers=headers, params=params, json=data, auth=self.auth
        )
        return res.json()

    def request_put(self, path, params=None, data=None):
        """Wrapper on any put requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.
            data (dict, optional): Payload to send with request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.put(
            request_url, headers=headers, params=params, json=data, auth=self.auth
        )
        return res.json()

    def request_del(self, path, params=None, data=None):
        """Wrapper on any delete requests

        Args:
            path (str): Path to API endpoint e.g. /api/manualimport
            params (dict, optional): URL Parameters to send with the request. Defaults to None.
            data (dict, optional): Payload to send with request. Defaults to None.

        Returns:
            Object: Response object from requests
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.delete(
            request_url, headers=headers, params=params, json=data, auth=self.auth
        )
        return res.json()
