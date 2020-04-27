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

            args:
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

    def getCommand(self):
        """getCommand Queries the status of a previously 
            started command, or all currently started commands.

            Returns:
                json response

        """
        path = '/api/command'

        res = self.request_get(path)
        return res.json()

    def setCommand(self, **kwargs):
        """setCommand runs the specified command aginst Radarr.

            Parameters:
                cmdName - Name of the command to run
            Returns:
                json response

        """
        possibleCommands = {
            'RefreshMovie',
            'MoviesSearch',
            'DownloadedMoviesScan',
            'RssSync',
            'RenameFiles',
            'RenameMovie',
            'CutOffUnmetMoviesSearch',
            'NetImportSync',
            'missingMoviesSearch'
        }
        data = {}
        if len(kwargs) >= 1:
            for key, value in kwargs.items():
                print("{0} = {1}".format(key, value))
            name = kwargs['Name']
            
            if name in possibleCommands:
                data.update({
                    'name': name
                })

                path = '/api/command'
                res = self.request_post(path, data)
                return res.json()

