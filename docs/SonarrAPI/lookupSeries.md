---
layout: default
title: lookupSeries
parent: SonarrAPI
nav_order: 4
---

## Summary

Searches for new shows on TheTVDB.com utilizing sonarr.tv's caching and augmentation proxy.

## Parameters

Required: None

- One of the following:
  - `"the walking dead"` Enter the Series Name
  - `266189` Enter the series TVDB ID

Optional: None

## Example

```python
lookupSeries()
```

```python
lookupSeries('"the walking dead"')
```

```python
lookupSeries(266189)
```

## Returns JsonArray

```json
[
  {
    "title": "The Walking Dead",
    "sortTitle": "walking dead",
    "seasonCount": 10,
    "status": "continuing",
    "overview": "The world we knew is gone. An epidemic of apocalyptic proportions has swept the globe causing the dead to rise and feed on the living. In a matter of months society has crumbled. In a world ruled by the dead, we are forced to finally start living. Based on a comic book series of the same name by Robert Kirkman, this AMC project focuses on the world after a zombie apocalypse. The series follows a police officer, Rick Grimes, who wakes up from a coma to find the world ravaged with zombies. Looking for his family, he and a group of survivors attempt to battle against the zombies in order to stay alive.",
    "network": "AMC",
    "airTime": "21:00",
    "images": [
      {
        "coverType": "fanart",
        "url": "https://artworks.thetvdb.com/banners/fanart/original/153021-83.jpg"
      },
      {
        "coverType": "banner",
        "url": "https://artworks.thetvdb.com/banners/graphical/153021-g39.jpg"
      },
      {
        "coverType": "poster",
        "url": "https://artworks.thetvdb.com/banners/posters/153021-6.jpg"
      }
    ],
    "remotePoster": "https://artworks.thetvdb.com/banners/posters/153021-6.jpg",
    "seasons": [
      { "seasonNumber": 0, "monitored": False },
      { "seasonNumber": 1, "monitored": True },
      { "seasonNumber": 2, "monitored": True },
      { "seasonNumber": 3, "monitored": True },
      { "seasonNumber": 4, "monitored": True },
      { "seasonNumber": 5, "monitored": True },
      { "seasonNumber": 6, "monitored": True },
      { "seasonNumber": 7, "monitored": True },
      { "seasonNumber": 8, "monitored": True },
      { "seasonNumber": 9, "monitored": True },
      { "seasonNumber": 10, "monitored": True }
    ],
    "year": 2010,
    "profileId": 0,
    "seasonFolder": False,
    "monitored": True,
    "useSceneNumbering": False,
    "runtime": 45,
    "tvdbId": 153021,
    "tvRageId": 25056,
    "tvMazeId": 73,
    "firstAired": "2010-10-10T23:00:00Z",
    "seriesType": "standard",
    "cleanTitle": "thewalkingdead",
    "imdbId": "tt1520211",
    "titleSlug": "the-walking-dead",
    "certification": "TV-MA",
    "genres": ["Adventure", "Drama", "Horror", "Thriller"],
    "tags": [],
    "added": "0001-01-01T00:00:00Z",
    "ratings": { "votes": 41187, "value": 9.0 },
    "qualityProfileId": 0
  }
]
```
