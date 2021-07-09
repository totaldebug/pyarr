import requests


class RequestAPI:
    """Base class for API wrappers."""

    def __init__(
        self,
        host_url: str,
        api_key: str,
    ):
        """Constructor requires Host-URL and API-KEY

        Args:
            host_url (str) - Host url to sonarr.
            api_key: API key from Sonarr. You can find this
        """
        self.host_url = host_url
        self.api_key = api_key
        self.session = requests.Session()
        self.auth = None

    def basic_auth(self, username, password):
        """If you have basic authentication setup you will need to pass your
        username and passwords to the requests.auth.HTTPBASICAUTH() method.

        Args:
            username (str) - Username for the basic auth requests.
            password (str) - Password for the basic auth requests.

        Return:
            requests.auth.HTTPBASICAUTH
        """
        self.auth = requests.auth.HTTPBasicAuth(username, password)
        return self.auth

    def request_get(self, path, params=None):
        """Wrapper on the session.get
        Args:
            path (str) - Path to API. E.g. /api/manualimport
            params (dict) - URL Parameters to send with the request
            data (dict) - Payload to send with request.
        Returns:
            requests.models.Response: Response object form requests.
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.get(
            request_url, headers=headers, params=params, auth=self.auth
        )
        return res.json()

    def request_post(self, path, params=None, data=None):
        """Wrapper on the requests.post

        Args:
            path (str) - Path to API. E.g. /api/manualimport
            params (dict) - URL Parameters to send with the request
            data (dict) - Payload to send with request.
        Returns:
            requests.models.Response: Response object form requests.
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.post(
            request_url, headers=headers, params=params, json=data, auth=self.auth
        )
        return res.json()

    def request_put(self, path, params=None, data=None):
        """Wrapper on the requests.put

        Args:
            path (str) - Path to API. E.g. /api/manualimport
            params (dict) - URL Parameters to send with the request
            data (dict) - Payload to send with request.
        Returns:
            requests.models.Response: Response object form requests.
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.put(
            request_url, headers=headers, params=params, json=data, auth=self.auth
        )
        return res.json()

    def request_del(self, path, params=None, data=None):
        """Wrapper on the requests.delete

        Args:
            path (str) - Path to API. E.g. /api/manualimport
            params (dict) - URL Parameters to send with the request
            data (dict) - Payload to send with request.
        Returns:
            requests.models.Response: Response object form requests.
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.delete(
            request_url, headers=headers, params=params, json=data, auth=self.auth
        )
        return res.json()
