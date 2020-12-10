---
layout: default
title: movie
parent: RadarrAPIv1
nav_order: 4
---

# get_movie

## Summary

Returns Movies in your collection

## Parameters

Required:

- None

Optional:

- `tmdbid(int)` - returns movie with the matching ID


## Example

```python
get_movie()
```

```python
get_movie(1234)
```

## Returns JsonArray

```json
[
    {
        'path': '/',
        'label': '',
        'freeSpace': 10056593408,
        'totalSpace': 10726932480
    }
]
```

# lookup_movie

## Summary

Searches for new movies on trakt

## Parameters

Required:
  - `term` = Enter the Movie's Name

Optional:


## Example

```python
lookup_movie('Star Wars')
```

## Returns JsonArray

```json
{
    'title': 'Solo: A Star Wars Story',
    'alternativeTitles': [],
    'secondaryYearSourceId': 0,
    'sortTitle': 'solo star wars story',
    'sizeOnDisk': 0,
    'status': 'released',
    'overview': 'Through a series of daring escapades deep within a dark and dangerous criminal underworld Han Solo meets his mighty future copilot Chewbacca and encounters the notorious gambler Lando Calrissian.',
    'inCinemas': '2018-05-15T00:00:00Z',
    'images': [
        {
            'coverType': 'poster',
            'url': 'http://image.tmdb.org/t/p/original/4oD6VEccFkorEBTEDXtpLAaz0Rl.jpg'
        }
    ],
    'downloaded': False,
    'year': 2018,
    'hasFile': False,
    'profileId': 0,
    'pathState': 'dynamic',
    'monitored': False,
    'minimumAvailability': 'tba',
    'isAvailable': True,
    'folderName': '',
    'runtime': 0,
    'tmdbId': 348350,
    'titleSlug': 'solo-a-star-wars-story-348350',
    'genres': [],
    'tags': [],
    'added': '0001-01-01T00:00:00Z',
    'ratings': {
        'votes': 5152,
        'value': 6.6
    },
    'qualityProfileId': 0
}
```



# add_movie

## Summary

Adds a new movie to your collection

## Parameters

Required:
- dbid = TMDB id
- qualityProfileId = Quailty Profle ID

Optional:
- rootDir = the root directory for the file (Defaults to primary dir)
- monitored = Default: True
- searchForMovie = Default: True
## Example

```python
add_movie('348350', 1)
```

## Returns JsonArray

```json
{
    'title': 'Solo: A Star Wars Story',
    'alternativeTitles': [],
    'secondaryYearSourceId': 0,
    'sortTitle': 'solo star wars story',
    'sizeOnDisk': 0,
    'status': 'tba',
    'images': [
        {
            'coverType': 'poster',
            'url': '/MediaCover/243/poster.jpg'
        }
    ],
    'downloaded': False,
    'year': 2018,
    'hasFile': False,
    'path': '/movies/Solo: A Star Wars Story',
    'profileId': 1,
    'pathState': 'static',
    'monitored': True,
    'minimumAvailability': 'tba',
    'isAvailable': True,
    'folderName': '/movies/Solo: A Star Wars Story',
    'runtime': 0,
    'cleanTitle': 'solostarwarsstory',
    'tmdbId': 348350,
    'titleSlug': 'solo-a-star-wars-story-348350',
    'genres': [],
    'tags': [],
    'added': '2020-04-29T09:28:54.179226Z',
    'addOptions': {
        'searchForMovie': True,
        'ignoreEpisodesWithFiles': False,
        'ignoreEpisodesWithoutFiles': False
    },
    'qualityProfileId': 1,
    'id': 243
}
```

# upd_movie

## Summary

Update the information of a movie currently within Radarr.

## Parameters

Required: data (object obtained by getMovie())

## Example

```python
movie = getMovie(radarr_id)
movie["monitored"] = True
upd_movie(movie)
```

## Returns Json

```json
{'added': '2020-09-27T17:48:20.5583865Z',
 'alternativeTitles': [{'id': 42,
                        'language': {'id': 1, 'name': 'English'},
                        'movieId': 5,
                        'sourceId': 0,
                        'sourceType': 'tmdb',
                        'title': 'Grandes Héroes',
                        'voteCount': 0,
                        'votes': 0},
                       {'id': 43,
                        'language': {'id': 1, 'name': 'English'},
                        'movieId': 5,
                        'sourceId': 0,
                        'sourceType': 'tmdb',
                        'title': '大英雄联盟',
                        'voteCount': 0,
                        'votes': 0},
                       {'id': 44,
                        'language': {'id': 1, 'name': 'English'},
                        'movieId': 5,
                        'sourceId': 0,
                        'sourceType': 'tmdb',
                        'title': '6 kangelast',
                        'voteCount': 0,
                        'votes': 0},
                       {'id': 45,
                        'language': {'id': 2, 'name': 'French'},
                        'movieId': 5,
                        'sourceId': 0,
                        'sourceType': 'tmdb',
                        'title': 'Les Nouveaux Heros',
                        'voteCount': 0,
                        'votes': 0},
                       {'id': 46,
                        'language': {'id': 1, 'name': 'English'},
                        'movieId': 5,
                        'sourceId': 0,
                        'sourceType': 'tmdb',
                        'title': '6 Giborim',
                        'voteCount': 0,
                        'votes': 0},
                       {'id': 47,
                        'language': {'id': 1, 'name': 'English'},
                        'movieId': 5,
                        'sourceId': 0,
                        'sourceType': 'tmdb',
                        'title': 'ベイマックス',
                        'voteCount': 0,
                        'votes': 0},
                       {'id': 48,
                        'language': {'id': 1, 'name': 'English'},
                        'movieId': 5,
                        'sourceId': 0,
                        'sourceType': 'tmdb',
                        'title': '빅 히어로',
                        'voteCount': 0,
                        'votes': 0},
                       {'id': 49,
                        'language': {'id': 15, 'name': 'Norwegian'},
                        'movieId': 5,
                        'sourceId': 0,
                        'sourceType': 'tmdb',
                        'title': 'Disney Klassiker 53 - Big Hero 6',
                        'voteCount': 0,
                        'votes': 0},
                       {'id': 50,
                        'language': {'id': 11, 'name': 'Russian'},
                        'movieId': 5,
                        'sourceId': 0,
                        'sourceType': 'tmdb',
                        'title': 'Город героев',
                        'voteCount': 0,
                        'votes': 0}],
 'certification': 'PG',
 'cleanTitle': 'bighero6',
 'downloaded': True,
 'folderName': '/media/Movies/Big Hero 6 (2014)',
 'genres': ['Adventure', 'Family', 'Animation'],
 'hasFile': True,
 'id': 5,
 'images': [{'coverType': 'poster',
             'remoteUrl': 'https://image.tmdb.org/t/p/original/2mxS4wUimwlLmI1xp6QW6NSU361.jpg',
             'url': '/MediaCover/5/poster.jpg?lastWrite=637368257018459301'},
            {'coverType': 'fanart',
             'remoteUrl': 'https://image.tmdb.org/t/p/original/4s2d3xdyqotiVNHTlTlJjrr3q0H.jpg',
             'url': '/MediaCover/5/fanart.jpg?lastWrite=637368257026829482'}],
 'imdbId': 'tt2245084',
 'inCinemas': '2014-10-24T00:00:00Z',
 'isAvailable': True,
 'lastInfoSync': '2020-09-27T17:48:21.0322258Z',
 'minimumAvailability': 'announced',
 'monitored': True,
 'movieFile': {'dateAdded': '2020-09-27T17:48:21.1615426Z',
               'edition': '',
               'id': 4,
               'mediaInfo': {'audioAdditionalFeatures': 'LC',
                             'audioBitrate': 93624,
                             'audioChannelPositions': '2/0/0',
                             'audioChannelPositionsText': 'Front: L R',
                             'audioChannels': 2,
                             'audioCodecID': 'mp4a-40-2',
                             'audioCodecLibrary': '',
                             'audioFormat': 'AAC',
                             'audioLanguages': 'English',
                             'audioProfile': '',
                             'audioStreamCount': 1,
                             'containerFormat': 'MPEG-4',
                             'height': 808,
                             'runTime': '01:41:52.6880000',
                             'scanType': 'Progressive',
                             'schemaRevision': 5,
                             'subtitles': '',
                             'videoBitDepth': 8,
                             'videoBitrate': 2215000,
                             'videoCodecID': 'avc1',
                             'videoCodecLibrary': 'x264 - core 142 r2479 '
                                                  'dd79a61',
                             'videoColourPrimaries': 'BT.709',
                             'videoFormat': 'AVC',
                             'videoFps': 23.976,
                             'videoMultiViewCount': 0,
                             'videoProfile': 'High@L4.1',
                             'videoTransferCharacteristics': '',
                             'width': 1920},
               'movieId': 0,
               'quality': {'quality': {'id': 7,
                                       'modifier': 'none',
                                       'name': 'Bluray-1080p',
                                       'resolution': 1080,
                                       'source': 'bluray'},
                           'revision': {'isRepack': False,
                                        'real': 0,
                                        'version': 1}},
               'relativePath': 'Big Hero 6 (2014) Bluray-1080p.mp4',
               'size': 1766948530},
 'overview': 'The special bond that develops between plus-sized inflatable '
             'robot Baymax, and prodigy Hiro Hamada, who team up with a group '
             'of friends to form a band of high-tech heroes.',
 'path': '/media/Movies/Big Hero 6 (2014)',
 'physicalRelease': '2015-02-24T00:00:00Z',
 'profileId': 1,
 'qualityProfileId': 1,
 'ratings': {'value': 7.8, 'votes': 12090},
 'runtime': 102,
 'secondaryYearSourceId': 0,
 'sizeOnDisk': 1766948530,
 'sortTitle': 'big hero 6',
 'status': 'released',
 'studio': 'Walt Disney Animation Studios',
 'tags': [],
 'title': 'Big Hero 6',
 'titleSlug': '177572',
 'tmdbId': 177572,
 'website': 'http://movies.disney.com/big-hero-6',
 'year': 2014,
 'youTubeTrailerId': 'vco0SpSz17g'}
```


# del_movie

## Summary

Delete the movie with the given ID

## Parameters

Required:

- `id (int)` Movie ID from Radarr

Optional:

- `delFiles (bool)`  if true the movie folder and all files will be deleted when the movie is deleted
- `addException (bool)` if true the movie TMDBID will be added to the import exclusions list when the movie is deleted

## Example

```python
del_movie(1)
```

## Returns JsonArray

```json
{}
```
