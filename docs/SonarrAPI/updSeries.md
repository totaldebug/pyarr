---
layout: default
title: updSeries
parent: SonarrAPI
nav_order: 4
---

## Summary

Update an existing series currently within Sonarr.

## Parameters

Required: data (object obtained by getSeries())

## Example

```python
series = getSeries(series_id)
series["seriesType"] = "Anime"
updSeries(series)
```

## Returns Json

```json
{'added': '2020-09-09T05:51:51.903196Z',
 'airTime': '17:30',
 'alternateTitles': [{'sceneSeasonNumber': -1,
                      'title': 'Boku no Hero Academia'},
                     {'sceneSeasonNumber': 3, 'title': 'My Hero Academia S3'},
                     {'sceneSeasonNumber': 2, 'title': 'My Hero Academia S2'},
                     {'sceneSeasonNumber': 3,
                      'title': 'My Hero Academia 3rd Season'},
                     {'sceneSeasonNumber': 4, 'title': 'My Hero Academia S4'},
                     {'sceneSeasonNumber': 4,
                      'title': 'Boku No Hero Academia (2019)'},
                     {'sceneSeasonNumber': 4,
                      'title': 'My Hero Academia 4th Season'},
                     {'sceneSeasonNumber': 4, 'title': 'My Hero Academy S4'},
                     {'sceneSeasonNumber': 3, 'title': 'My Hero Academy S3'},
                     {'sceneSeasonNumber': 2, 'title': 'My Hero Academy S2'},
                     {'sceneSeasonNumber': 4,
                      'title': 'Boku no Hero Academia S4'},
                     {'sceneSeasonNumber': 3,
                      'title': 'Boku no Hero Academia S3'},
                     {'sceneSeasonNumber': 2,
                      'title': 'Boku no Hero Academia S2'},
                     {'sceneSeasonNumber': 4,
                      'title': 'Boku no Hero Academia 4th Season'},
                     {'sceneSeasonNumber': 3,
                      'title': 'Boku no Hero Academia 3rd Season'},
                     {'sceneSeasonNumber': 2,
                      'title': 'My Hero Academia 2nd Season'}],
 'certification': 'TV-14',
 'cleanTitle': 'myheroacademia',
 'episodeCount': 88,
 'episodeFileCount': 84,
 'firstAired': '2016-04-03T07:00:00Z',
 'genres': ['Action', 'Adventure', 'Animation', 'Anime', 'Comedy', 'Fantasy'],
 'id': 5,
 'images': [{'coverType': 'banner',
             'remoteUrl': 'https://artworks.thetvdb.com/banners/graphical/305074-g.jpg',
             'url': '/MediaCover/5/banner.jpg?lastWrite=637352275136732840'},
            {'coverType': 'poster',
             'remoteUrl': 'https://artworks.thetvdb.com/banners/posters/305074-5.jpg',
             'url': '/MediaCover/5/poster.jpg?lastWrite=637352275141422940'},
            {'coverType': 'fanart',
             'remoteUrl': 'https://artworks.thetvdb.com/banners/fanart/original/305074-4.jpg',
             'url': '/MediaCover/5/fanart.jpg?lastWrite=637352275146583050'}],
 'imdbId': 'tt5626028',
 'languageProfileId': 1,
 'lastInfoSync': '2020-09-27T16:58:37.747572Z',
 'monitored': True,
 'network': 'Nippon TV',
 'overview': 'Izuku has dreamt of being a hero all his life—a lofty goal for '
             'anyone, but especially challenging for a kid with no '
             'superpowers. That’s right, in a world where eighty percent of '
             'the population has some kind of super-powered “quirk,” Izuku was '
             'unlucky enough to be born completely normal. But that’s not '
             'enough to stop him from enrolling in one of the world’s most '
             'prestigious hero academies.',
 'path': '/media/TV/My Hero Academia',
 'previousAiring': '2020-04-04T21:30:00Z',
 'profileId': 1,
 'qualityProfileId': 1,
 'ratings': {'value': 8.8, 'votes': 859},
 'runtime': 25,
 'seasonCount': 4,
 'seasonFolder': True,
 'seasons': [{'monitored': False,
              'seasonNumber': 0,
              'statistics': {'episodeCount': 0,
                             'episodeFileCount': 0,
                             'percentOfEpisodes': 0.0,
                             'sizeOnDisk': 0,
                             'totalEpisodeCount': 9}},
             {'monitored': True,
              'seasonNumber': 1,
              'statistics': {'episodeCount': 12,
                             'episodeFileCount': 12,
                             'percentOfEpisodes': 100.0,
                             'previousAiring': '2016-06-26T21:30:00Z',
                             'sizeOnDisk': 9202900588,
                             'totalEpisodeCount': 13}},
             {'monitored': True,
              'seasonNumber': 2,
              'statistics': {'episodeCount': 23,
                             'episodeFileCount': 23,
                             'percentOfEpisodes': 100.0,
                             'previousAiring': '2017-09-30T21:30:00Z',
                             'sizeOnDisk': 13469966037,
                             'totalEpisodeCount': 25}},
             {'monitored': True,
              'seasonNumber': 3,
              'statistics': {'episodeCount': 25,
                             'episodeFileCount': 25,
                             'percentOfEpisodes': 100.0,
                             'previousAiring': '2018-09-29T21:30:00Z',
                             'sizeOnDisk': 19980012802,
                             'totalEpisodeCount': 25}},
             {'monitored': True,
              'seasonNumber': 4,
              'statistics': {'episodeCount': 24,
                             'episodeFileCount': 24,
                             'percentOfEpisodes': 100.0,
                             'previousAiring': '2020-04-04T21:30:00Z',
                             'sizeOnDisk': 34785539617,
                             'totalEpisodeCount': 25}}],
 'seriesType': 'anime',
 'sizeOnDisk': 77438419044,
 'sortTitle': 'my hero academia',
 'status': 'continuing',
 'tags': [],
 'title': 'My Hero Academia',
 'titleSlug': 'my-hero-academia',
 'totalEpisodeCount': 97,
 'tvMazeId': 13615,
 'tvRageId': 0,
 'tvdbId': 305074,
 'useSceneNumbering': True,
 'year': 2016}
```
