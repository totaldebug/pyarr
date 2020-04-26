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
    
    #TODO: TEST
    def getCalendar(self, *args):
        """getCalendar retrieves info about when movies were/will be downloaded.
           If start and end are not provided, retrieves movies airing today and tomorrow.

            Kwargs:
                start_date (datetime):
                end_date (datetime): 
        
            Returns:
                json response

        """
        path = '/api/calendar'
        data = {}
        
        if len(args) == 2:
            start_date = args[0]
            end_date = args[1]
             
            if isinstance(start_date, datetime):
                startDate = start_date.strftime('%Y-%m-%d')
                data.update({
                    'start': startDate                
                })

            if isinstance(end_date, datetime):
                endDate = end_date.strftime('%Y-%m-%d') 
                data.update({
                    'end': endDate
                })

        res = self.request_get(path, **data)
        return res.json()