from urllib.parse import urlencode

import requests


class RequestAPI:
    def __init__(
        self,
        host_url: str,
        api_key: str,
    ):
        """Constructor requires Host-URL and API-KEY

        Args:
            host_url (str): Host url to sonarr.
            api_key: API key from Sonarr. You can find this
        """
        self.host_url = host_url
        self.api_key = api_key
        self.session = requests.Session()
        self.auth = None

    def basic_auth(self, username, password):
        """If you have basic authentication setup you will need to pass yourpyli
        username and passwords to the requests.auth.HTTPBASICAUTH() method.

        Args:
            username (str): Username for the basic auth requests.
            password (str): Password for the basic auth requests.

        Return:
            requests.auth.HTTPBASICAUTH
        """
        self.auth = requests.auth.HTTPBasicAuth(username, password)
        return self.auth

    def request_get(self, path, **kwargs):
        """Wrapper on the session.get
        Kwargs:
            **kwargs: Any url attributes to add to the request.

        Returns:
            requests.models.Response: Response object form requests.
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        try:
            if len(kwargs) >= 1:
                encoded_params = urlencode(kwargs)
                request_url = "{}?{}".format(request_url, encoded_params)
        except:
            pass

        res = self.session.get(request_url, headers=headers, auth=self.auth)
        return res

    def request_post(self, path, data):
        """Wrapper on the requests.post

        Args:
            path (str): Path to API. E.g. /api/manualimport
            data (dict): data payload to send with request.

        Returns:
            requests.models.Response: Response object form requests.
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.post(request_url, headers=headers, json=data, auth=self.auth)
        return res

    def request_put(self, path, data):
        """Wrapper on the requests.put

        Args:
            path (str): Path to API. E.g. /api/manualimport
            data (dict): data payload to send with request.

        Returns:
            requests.models.Response: Response object form requests.
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.put(request_url, headers=headers, json=data, auth=self.auth)
        return res

    def request_del(self, path, data):
        """Wrapper on the requests.delete

        Args:
            path (str): Path to API. E.g. /api/manualimport
            data (dict): data payload to send with request.

        Returns:
            res (Request Response Object)
        """
        headers = {"X-Api-Key": self.api_key}
        request_url = "{url}{path}".format(url=self.host_url, path=path)
        res = self.session.delete(
            request_url, headers=headers, json=data, auth=self.auth
        )
        return res
