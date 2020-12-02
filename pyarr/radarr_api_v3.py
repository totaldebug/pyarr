# -*- coding: utf-8 -*-

from datetime import datetime

from .request_api import RequestAPI


class RadarrAPIv3(RequestAPI):
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
    ## Movies
    # TODO: GET Movie
    # TODO: POST Movie
    # TODO: PUT Movie
    # TODO: DELETE Movie
    # TODO: GET Movie Lookup
    # TODO: PUT Movie Editor
    # TODO: DELETE Movie Editor
    # TODO: POST Movie import

    ## Movie Files
    # TODO: GET movieFiles
    # TODO: GET Movie File
    # TODO: DELETE Movie Files

    ## history
    # TODO: GET history
    # TODO: GET History Movies

    ## blacklist
    # TODO: GET blacklist
    # TODO: DELETE blacklist
    # TODO: GET blacklist movie
    # TODO: DELETE Blacklist Bulk

    ## queue
    # TODO: GET Queue

    ## indexer
    # TODO: GET indexer
    # TODO: GET Indexer by ID
    # TODO: PUT Indexer by id
    # TODO: DELETE Indexer by id

    ## Download client

    ## Import Lists

    ## Notification

    ## Tag

    ## diskspace

    ## Settings

    ## metadata

    ## system

    ## health

    ## command

    ## update

    ## quality

    ## calendar

    ## custom filters

    ## remote path mapping

