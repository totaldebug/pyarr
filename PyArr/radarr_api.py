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

    def getCommand(self, *args):
        """getCommand Queries the status of a previously 
            started command, or all currently started commands.
            
            Args:
                Optional - id (int) Unique ID of command
            Returns:
                json response

        """
        if len(args) == 1:
            path = f'/api/command/{args[0]}'
        else:
            path = '/api/command'

        res = self.request_get(path)
        return res.json()

    def __setCommand(self, data):
        """Private Command Method

            Args:
                data (dict): data payload to send to /api/command

            Returns:
                json response
        """
        path = '/api/command'
        res = self.request_post(path, data)
        return res.json()   

    def RefreshMovie(self, *args):
        """RefreshMovie refreshes movie information and rescans disk.

            Args:
                Optional - movieId (int)        
            Returns:
                json response

        """
        data = {}
        if len(args) == 1: 
            data.update({
                'name': 'RefreshMovie',
                'movieId': args[0]
            })
        else:
            data.update({
                'name': 'RefreshMovie'
            })
        return self.__setCommand(data)

    def RescanMovie(self, *args):
        """RescanMovie scans disk for any downloaded movie for all or specified movie.

            Args:
                Optional - movieId (int)        
            Returns:
                json response

        """
        data = {}
        if len(args) == 1: 
            data.update({
                'name': 'RescanMovie',
                'movieId': args[0]
            })
        else:
            data.update({
                'name': 'RescanMovie'
            })
        return self.__setCommand(data)
    
    def getDiskSpace(self):
        """GetDiskSpace retrieves info about the disk space on the server.
            
            Args: 
                None
            Returns:
                json response

        """
        path = '/api/diskspace'
        res = self.request_get(path)
        return res.json()    

    def getMovie(self, *args):
        """getMovie returns all movies in collection.
            
            Args: 
                Optional - id (int) ID of movie
            Returns:
                json response

        """
        movieId = args[0]

        if len(movieId) == 1 and isinstance(movieId, (int)): 
            path = f'/api/movie/{movieId}'
        else:
            path = '/api/movie'
        
        res = self.request_get(path)
        return res.json()   

    def lookupMovie(self, term):
        """lookupMovie serches for movie
            
            Args: 
                Requried - term / tmdbId / imdbId
            Returns:
                json response

        """
        term = str(term)

        if term.isdigit():
            path = f'/api/movie/lookup/tmdb?tmdbId={term}'
            print(path)
        elif term.startswith('tt'):
            path = f'/api/movie/lookup/imdb?imdbId={term}'
        else:
            term = term.replace(' ', '%20')
            path = f'/api/movie/lookup?term={term}'

        res = self.request_get(path)
        return res.json()  

    def constructMovieJson(self, tmdbId, qualityProfileId ):
        """Searches for movie on tmdb and returns Movie json to add"""
        
        res = self.lookupMovie(tvdbId)
        s_dict = res[0]

        # get root folder path
        root = self.get_root_folder()[0]['path']
        series_json = {
            'title': s_dict['title'],
            'seasons': s_dict['seasons'],
            'path': root + s_dict['title'],
            'qualityProfileId': quality_profile,
            'seasonFolder': True,
            'monitored': True,
            'tvdbId': tvdbId,
            'images': s_dict['images'],
            'titleSlug': s_dict['titleSlug'],
            "addOptions": {
                          "ignoreEpisodesWithFiles": True,
                          "ignoreEpisodesWithoutFiles": True
                        }
                    }
        return series_json

    def addMovie(self, *args):
        """addMovie adds a new movie to collection
            
            Args: 
                tmdbid
            Returns:
                json response

        """

        self.constructMovieJson(tmdbId, qualityProfileId)
