---
layout: default
title: getSeries
parent: SonarrAPI
nav_order: 4
---

## Summary

Returns all series in your collection

## Parameters

Required:

- None

Optional:

- `id (int)` Series ID from Sonarr

## Example

```python
getSeries()
```
```python
getSeries(1)
```

## Returns JsonArray

```json
[
  {
    "title": "Marvel's Daredevil",
    "alternateTitles": [{
      "title": "Daredevil",
      "seasonNumber": -1
    }],
    "sortTitle": "marvels daredevil",
    "seasonCount": 2,
    "totalEpisodeCount": 26,
    "episodeCount": 26,
    "episodeFileCount": 26,
    "sizeOnDisk": 79282273693,
    "status": "continuing",
    "overview": "Matt Murdock was blinded in a tragic accident as a boy, but imbued with extraordinary senses. Murdock sets up practice in his old neighborhood of Hell's Kitchen, New York, where he now fights against injustice as a respected lawyer by day and as the masked vigilante Daredevil by night.",
    "previousAiring": "2016-03-18T04:01:00Z",
    "network": "Netflix",
    "airTime": "00:01",
    "images": [{
      "coverType": "fanart",
      "url": "/sonarr/MediaCover/7/fanart.jpg?lastWrite=636072351904299472"
    },
    {
      "coverType": "banner",
      "url": "/sonarr/MediaCover/7/banner.jpg?lastWrite=636071666185812942"
    },
    {
      "coverType": "poster",
      "url": "/sonarr/MediaCover/7/poster.jpg?lastWrite=636071666195067584"
    }],
    "seasons": [{
      "seasonNumber": 1,
      "monitored": false,
      "statistics": {
        "previousAiring": "2015-04-10T04:01:00Z",
        "episodeFileCount": 13,
        "episodeCount": 13,
        "totalEpisodeCount": 13,
        "sizeOnDisk": 22738179333,
        "percentOfEpisodes": 100
      }
    },
    {
      "seasonNumber": 2,
      "monitored": false,
      "statistics": {
        "previousAiring": "2016-03-18T04:01:00Z",
        "episodeFileCount": 13,
        "episodeCount": 13,
        "totalEpisodeCount": 13,
        "sizeOnDisk": 56544094360,
        "percentOfEpisodes": 100
      }
    }],
    "year": 2015,
    "path": "F:\\TV_Shows\\Marvels Daredevil",
    "profileId": 6,
    "seasonFolder": true,
    "monitored": true,
    "useSceneNumbering": false,
    "runtime": 55,
    "tvdbId": 281662,
    "tvRageId": 38796,
    "tvMazeId": 1369,
    "firstAired": "2015-04-10T04:00:00Z",
    "lastInfoSync": "2016-09-09T09:02:49.4402575Z",
    "seriesType": "standard",
    "cleanTitle": "marvelsdaredevil",
    "imdbId": "tt3322312",
    "titleSlug": "marvels-daredevil",
    "certification": "TV-MA",
    "genres": ["Action",
    "Crime",
    "Drama"],
    "tags": [],
    "added": "2015-05-15T00:20:32.7892744Z",
    "ratings": {
      "votes": 461,
      "value": 8.9
    },
    "qualityProfileId": 6,
    "id": 7
  }
]
```
