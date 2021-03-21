---
layout: default
title: upd_episode
parent: SonarrAPI
nav_order: 4
---

## Summary

Update an existing episode currently within Sonarr.

## Parameters

Required: data (object obtained by `getEpisodesBySeriesId()` or `getEpisodeByEpisodeId()`)

## Example

```python
episode = getEpisodesByEpisodeId(3807)
episode["monitored"] = True
upd_episode(episode)
```

## Returns Json

```json
[{'absoluteEpisodeNumber': 10,
  'airDate': '2016-06-05',
  'airDateUtc': '2016-06-05T21:30:00Z',
  'episodeFileId': 0,
  'episodeNumber': 10,
  'hasFile': False,
  'id': 3807,
  'lastSearchTime': '2020-09-27T18:10:48.810014Z',
  'monitored': True,
  'overview': "Villains have attacked USJ, and it's up to Class 1-A to stop "
              'them. What are the villains after? Will All Might be able to '
              'save the day again?',
  'sceneAbsoluteEpisodeNumber': 10,
  'sceneEpisodeNumber': 10,
  'sceneSeasonNumber': 1,
  'seasonNumber': 1,
  'series': {'added': '2020-09-09T05:51:51.903196Z',
             'airTime': '17:30',
             'certification': 'TV-14',
             'cleanTitle': 'myheroacademia',
             'firstAired': '2016-04-03T07:00:00Z',
             'genres': ['Action',
                        'Adventure',
                        'Animation',
                        'Anime',
                        'Comedy',
                        'Fantasy'],
             'id': 5,
             'images': [{'coverType': 'banner',
                         'url': 'https://artworks.thetvdb.com/banners/graphical/305074-g.jpg'},
                        {'coverType': 'poster',
                         'url': 'https://artworks.thetvdb.com/banners/posters/305074-5.jpg'},
                        {'coverType': 'fanart',
                         'url': 'https://artworks.thetvdb.com/banners/fanart/original/305074-4.jpg'}],
             'imdbId': 'tt5626028',
             'languageProfileId': 1,
             'lastInfoSync': '2020-09-27T16:58:37.747572Z',
             'monitored': True,
             'network': 'Nippon TV',
             'overview': 'Izuku has dreamt of being a hero all his life—a '
                         'lofty goal for anyone, but especially challenging '
                         'for a kid with no superpowers. That’s right, in a '
                         'world where eighty percent of the population has '
                         'some kind of super-powered “quirk,” Izuku was '
                         'unlucky enough to be born completely normal. But '
                         'that’s not enough to stop him from enrolling in one '
                         'of the world’s most prestigious hero academies.',
             'path': '/media/TV/My Hero Academia',
             'profileId': 1,
             'qualityProfileId': 1,
             'ratings': {'value': 8.8, 'votes': 859},
             'runtime': 25,
             'seasonCount': 4,
             'seasonFolder': True,
             'seasons': [{'monitored': False, 'seasonNumber': 0},
                         {'monitored': True, 'seasonNumber': 1},
                         {'monitored': True, 'seasonNumber': 2},
                         {'monitored': True, 'seasonNumber': 3},
                         {'monitored': True, 'seasonNumber': 4}],
             'seriesType': 'anime',
             'sortTitle': 'my hero academia',
             'status': 'continuing',
             'tags': [],
             'title': 'My Hero Academia',
             'titleSlug': 'my-hero-academia',
             'tvMazeId': 13615,
             'tvRageId': 0,
             'tvdbId': 305074,
             'useSceneNumbering': True,
             'year': 2016},
  'seriesId': 5,
  'title': 'Encounter With the Unknown',
  'unverifiedSceneNumbering': False}]
```
