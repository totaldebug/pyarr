# -*- coding: utf-8 -*-

from datetime import datetime

from .request_api import RequestAPI


class SonarrAPI(RequestAPI):

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
        super().__init__(host_url, api_key)

    def get_calendar(self, **kwargs):
        """Gets upcoming episodes, if start/end are not supplied episodes 
        airing today and tomorrow will be returned

            Kwargs:
                start_date (datetime):
                end_date (datetime): 
        
            Returns:
                requests.models.Response: Response object form requests.

        """
        path = '/api/calendar'
        data = {}
        if isinstance(kwargs['start_date'], datetime):
            date = kwargs['start_date'].strftime('%Y-%m-%dT%H:%M:%S.000Z') 
            data.update({
                'start': date
            })

        if isinstance(kwargs['end_date'], datetime):
            date = kwargs['end_date'].strftime('%Y-%m-%dT%H:%M:%S.000Z') 
            data.update({
                'end': date
            })

        res = self.request_get(path, **data)
        return res


    def command(self, data):
        """Command Method

            Args:
                data (dict): data payload to send to /api/command

            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/command'
        res = self.request_post(path, data)
        return res        

    @staticmethod
    def _build_manual_import_request(manual_dict):
        """This will build the request to post to /api/command for manual
        imports. Filter the episodes you want to process from /api/manualimport
        and pass the dictionary here. This will generate your data response for
        the method command().

            Args:
                manual_dict (dict): Pass a filtered dict from manual_import 
                method
            
            Returns:
                data (dict): Returns the data dictionary used to pass to the 
                command method.

        """
        data = {
            'name': 'manualImport',
            'files': [],
            'importMode': 'Move'
        }
        for episode in manual_dict:
            try:
                episode_ids = [ep['id'] for ep in episode['episodes']]
            except:
                print(episode)
                
            path = episode['path']
            series_id = episode['episodes'][0]['seriesId']
            
            data['files'].append({
                'path': path,
                'seriesId': series_id,
                'episodeIds': episode_ids,
                'quality': episode['quality']
            })
        return data
     
    def manual_import(self, **kwargs):
        """Manual import command
            Kwargs:
                folder (str): Folder to manually look at. Default is '/'.
                sort_by (str): What field to sort by. Default is 
                'qualityWeight'.
                order (str): desc or asc. Default is 'desc' 
            
            Returns:
                requests.models.Response: Response object form requests.
        
        """     
        url_params = {
            'folder': kwargs.get('folder', '/'),
            'sort_by': kwargs.get('sort_by', 'qualityWeight'),
            'order': kwargs.get('sort_by', 'desc'),
            'apikey': self.api_key
        }        
        
        path = '/api/manualimport'

        res = self.request_get(path, **url_params)
        return res

    def auto_manual_import(self, **kwargs):
        """Manual import command
            Kwargs:
                folder (str): Folder to manually look at.
                sort_by (str): What field to sort by.
                order (str): desc or asc. 
                verbose (bool): Want it to print out what episodes it found?

            Returns:
                requests.models.Response: Response object form requests.     
        """     
        verbose = kwargs.get('verbose', False)
        manual_import = self.manual_import(**kwargs)
        mi_dict = manual_import.json()
        rejections = [data for data in mi_dict if len(data['rejections']) < 1]

        if verbose:
            for episode in rejections:
                print(episode['name'])

        data = self._build_manual_import_request(rejections)
        return self.command(data)

    def get_diskspace(self):
        """Return Information about Diskspace
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/diskspace'
        res = self.request_get(path)
        return res

    # TODO: Test this
    def get_episodes_by_series_id(self, series_id):
        """Returns all episodes for the given series
            Args:
                series_id (int):
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        data = {
            'seriesId': series_id
        }
        path = '/api/episode'
        res = self.request_get(path, **data)
        return res

    # TODO: Test this
    def get_episode_by_episode_id(self, episode_id):
        """Returns the episode with the matching id
            Args:
                episode_id (int): 
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/episode/{}'.format(episode_id)
        res = self.request_get(path)
        return res

    # TODO: Test this
    def upd_episode(self, data):
        """Update the given episodes, currently only monitored is changed, all 
        other modifications are ignored. All parameters (you should perform a 
        GET/{id} and submit the full body with the changes, as other values may 
        be editable in the future.

            Args: 
                data (dict): data payload

            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/episode'
        res = self.request_put(path, data)
        return res

    # TODO: Test this
    def get_episode_files_by_series_id(self, series_id):
        """Returns all episode files for the given series

            Args:
                series_id (int):
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        data = {
            'seriesId': series_id
        }
        path = '/api/episodefile'
        res = self.request_get(path, **data)
        return res

    # TODO: Test this
    def get_episode_file_by_episode_id(self, episode_id):
        """Returns the episode file with the matching id

            Kwargs:
                episode_id (int):

            Returns:
                requests.models.Response: Response object form requests.     
        """
        path = '/api/episodefile/{}'.format(episode_id)
        res = self.request_get(path)
        return res

    # TODO: Test this
    def rem_episode_file_by_episode_id(self, episode_id):
        """Delete the given episode file
        
            Kwargs:
                episode_id (str):

            Returns:
                requests.models.Response: Response object form requests. 
        """
        path = '/api/episodefile/{}'.format(episode_id)
        res = self.request_del(path, data=None)
        return res

    # TODO: Test this
    def get_logs(self, **kwargs):
        """Gets Sonarr Logs

            Kwargs;
                page (int): Page number. Default 1.
                page_size (int): How many records per page. Default 50.
                sort_key (str): What key to sort on. Default 'time'.
                sort_dir (str): What direction to sort asc or desc. Default 
                desc.
                filter_key (str): What key to filter on. Default None.
                filter_value (str): What to filter on (Warn, Info, Error, All).
                Default All.

            Returns:
                requests.models.Response: Response object form requests.        
        """
        data = {
            'page': kwargs.get('page', 1),
            'pageSize': kwargs.get('page_size', 50),
            'sortKey': kwargs.get('sort_key', 'time'),
            'sortDir': kwargs.get('sort_dir', 'desc'),
            'filterKey': kwargs.get('filter_key', None),
            'filterValue': kwargs.get('filter_value', None)
        }
        if 'All' in data['filterValue'] or 'all' in data['filterValue']:
            data['filterValue'] = None

        path = '/api/log'
        res = self.request_get(path, **data)
        return res

    # TODO: Work in progress.
    def serach_selected(self):
        pass

    # TODO: Test this
    def search_all_missing(self):
        """Gets all missing episodes and task's the indexer/downloader.
        
            Returns:
                requests.models.Response: Response object form requests. 
        """
        data = {
            'name': 'missingEpisodeSearch'
        }
        return self.command(data)


    # TODO: Test this
    def get_queue(self):
        """Gets current downloading info
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/queue'
        res = self.request_get(path)
        return res


    # TODO: Test this
    def get_quality_profiles(self):
        """Gets all quality profiles
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/profile'
        res = self.request_get(path)
        return res

    # TODO: Test this
    def push_release(self, **kwargs):
        """Notifies Sonarr of a new release.
            title: release name
            downloadUrl: .torrent file URL
            protocol: usenet / torrent
            publishDate: ISO8601 date string

            Kwargs:
                title (str): 
                downloadUrl (str):
                protocol (str):
                publishDate (str):

            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/release/push'
        res = self.request_post(path, data=kwargs)
        return res

    # TODO: Test this
    def get_root_folder(self):
        """Returns the Root Folder
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/rootfolder'
        res = self.request_get(path)
        return res

    # TODO: Test this
    def get_series(self):
        """Return all series in your collection
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/series'
        res = self.request_get(path)
        return res

    # TODO: Test this
    def get_series_by_series_id(self, series_id):
        """Return the series with the matching ID or 404 if no matching series 
        is found
        
            Args:
                series_id (int):

            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/series/{}'.format(series_id)
        res = self.request_get(path)
        return res

    # TODO: Test this
    def constuct_series_json(self, tvdbId, quality_profile):
        """Searches for new shows on trakt and returns Series object to add
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/series/lookup?term={}'.format('tvdbId:' + str(tvdbId))
        res = self.request_get(path)
        s_dict = res

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
            'addOptions': {
                          'ignoreEpisodesWithFiles': True,
                          'ignoreEpisodesWithoutFiles': True
                        }
                    }
        return series_json

    # TODO: Test this
    def add_series(self, series_json):
        """Add a new series to your collection
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/series'
        res = self.request_post(path, data=series_json)
        return res

    # TODO: Test this
    def upd_series(self, data):
        """Update an existing series
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/series'
        res = self.request_put(path, data)
        return res

    # TODO: Test this
    def rem_series(self, series_id, rem_files=False):
        """Delete the series with the given ID

            Returns:
                requests.models.Response: Response object form requests.
        """
        # File deletion does not work
        data = {
            # 'id': series_id,
            'deleteFiles': 'true'
        }
        path = '/api/series/{}'.format(series_id)
        res = self.request_del(path, data)
        return res

    # TODO: Test this
    def lookup_series(self, **kwargs):
        """Searches for new shows on trakt
        
            Kwargs:
                term (str): term filter for lookup_series.
                **kwargs: Any url attributes to add to the request.
        
            Returns:
                requests.models.Response: Response object form requests.
        """
        path = '/api/series/lookup'
        res = self.request_get(path, **kwargs)
        return res

    # TODO: Test this
    def get_system_status(self):
        """Returns the System Status"""
        path = '/system/status'
        res = self.request_get(path)
        return res