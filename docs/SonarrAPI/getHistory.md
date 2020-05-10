---
layout: default
title: getHistory
parent: SonarrAPI
nav_order: 4
---

## Summary

Gets history (grabs/failures/completed)

## Parameters

### Required:

`sortKey (string)` - series.title or date default=date

### Optional:

`page (int)` - 1-indexed
`pageSize (int)` - Default: 0
`sortDir (string)` - asc or desc - Default: asc
`episodeId (int)` - Filters to a specific episode ID

## Example

```python
getHistory()
```

```python
getHistory("sortKey"="series.title", "page"=1, "pageSize"=50, "sortDir"=desc)
```

## Returns JsonArray

```json
{
  "page": 1,
  "pageSize": 10,
  "sortKey": "date",
  "sortDirection": "descending",
  "totalRecords": 1,
  "records": [
    {
      "episodeId": 0,
      "movieId": 13,
      "seriesId": 0,
      "sourceTitle": "Minions 2015 720p BluRay DD-EX x264-xxxxxxxxxx",
      "quality": {
        "quality": {
          "id": 6,
          "name": "Bluray-720p"
        },
        "revision": {
          "version": 1,
          "real": 0
        }
      },
      "qualityCutoffNotMet": false,
      "date": "2017-01-24T14:57:05.134486Z",
      "downloadId": "xxxxxxxxxx",
      "eventType": "grabbed",
      "data": {
        "indexer": "xxxxxxxxxx",
        "nzbInfoUrl": "xxxxxxxxxx",
        "releaseGroup": "xxxxxxxxxx",
        "age": "457",
        "ageHours": "10973.2155929178",
        "ageMinutes": "658392.935575217",
        "publishedDate": "2015-10-25T09:44:09Z",
        "downloadClient": "xxxxxxxxxx",
        "size": "xxxxxxxxxx",
        "downloadUrl": "xxxxxxxxxx",
        "guid": "xxxxxxxxxx",
        "tvdbId": "0",
        "tvRageId": "0",
        "protocol": "2",
        "torrentInfoHash": null
      },
      "movie": {
        "title": "Minions",
        "sortTitle": "minions",
        "sizeOnDisk": 0,
        "status": "released",
        "overview": "Minions Stuart, Kevin and Bob are recruited by Scarlet Overkill, a super-villain who, alongside her inventor husband Herb, hatches a plot to take over the world.",
        "inCinemas": "2015-06-17T00:00:00Z",
        "images": [
          {
            "coverType": "poster",
            "url": "http://image.tmdb.org/t/p/original/q0R4crx2SehcEEQEkYObktdeFy.jpg"
          },
          {
            "coverType": "banner",
            "url": "http://image.tmdb.org/t/p/original/uX7LXnsC7bZJZjn048UCOwkPXWJ.jpg"
          }
        ],
        "website": "http://www.minionsmovie.com/",
        "downloaded": false,
        "year": 2015,
        "hasFile": false,
        "youTubeTrailerId": "jc86EFjLFV4",
        "studio": "Universal Pictures",
        "path": "/path/to/Minions (2015)",
        "profileId": 3,
        "monitored": true,
        "runtime": 91,
        "lastInfoSync": "2017-01-24T14:57:00.765931Z",
        "cleanTitle": "minions",
        "imdbId": "tt2293640",
        "tmdbId": 211672,
        "titleSlug": "minions-2015",
        "genres": ["Family", "Animation", "Adventure", "Comedy"],
        "tags": [],
        "added": "2017-01-24T14:57:00.42543Z",
        "ratings": {
          "votes": 2941,
          "value": 6.5
        },
        "alternativeTitles": [],
        "qualityProfileId": 3,
        "id": 13
      },
      "id": 9
    }
  ]
}
```
