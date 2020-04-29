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

    def refreshMovie(self, *args):
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

    def rescanMovie(self, *args):
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
        elif term.startswith('tt'):
            path = f'/api/movie/lookup/imdb?imdbId={term}'
        else:
            term = term.replace(' ', '%20')
            path = f'/api/movie/lookup?term={term}'
        res = self.request_get(path)
        return res.json()

    def getRoot(self):
        """Returns the Root Folder"""
        path = '/api/rootfolder'
        res = self.request_get(path)
        return res.json()

    def constructMovieJson(self, dbId, qualityProfileId):
        """Searches for movie on tmdb and returns Movie json to add
        
            Args:
                Required - dbID, <imdb or tmdb id>
                Required - qualityProfileId (int)
            
            Return:
                JsonArray
        
        """
        s_dict = self.lookupMovie(dbId)

        root = self.getRoot()[0]['path']
        movie_json = {
            'title': s_dict['title'],
            'path': root + s_dict['title'],
            'qualityProfileId': qualityProfileId,
            'profileId': qualityProfileId,
            'year': s_dict['year'],
            'tmdbId': s_dict['tmdbId'],
            'images': s_dict['images'],
            'titleSlug': s_dict['titleSlug'],
            'monitored': True,
            "addOptions": {
                          "searchForMovie": True
                        }
                    }
        return movie_json

    def addMovie(self, dbId, qualityProfileId):
        """addMovie adds a new movie to collection
            
            Args: 
                Required - dbid
                Required - qualityProfileId
            Returns:
                json response

        """
        movie_json = self.constructMovieJson(dbId, qualityProfileId)

        path = '/api/movie'
        res = self.request_post(path, data=movie_json)
        return res.json()

    def getSystemStatus(self):
        """Returns the System Status as json"""
        path = '/api/system/status'
        res = self.request_get(path)
        return res.json()
