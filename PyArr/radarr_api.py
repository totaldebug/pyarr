# -*- coding: utf-8 -*-

from datetime import datetime

from .request_api import RequestAPI


class RadarrAPI(RequestAPI):

    def __init__(
            self, 
            host_url: str, 
            api_key: str,
        ):
        """Constructor requires Host-URL and API-KEY

            Args:
                host_url (str): Host url to radarr.
                api_key: API key from Radarr. You can find this
        """
        super().__init__(host_url, api_key)
