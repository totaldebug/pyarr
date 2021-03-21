---
layout: default
title: get_queue
parent: SonarrAPI
nav_order: 4
---

## Summary

Gets queue info (downloading/completed, ok/warning)

## Parameters

Required:

- None

Optional:

- None

## Example

```python
getQueue()
```

## Returns JsonArray

```json
[
  {
    "series": {
      "title": "Transplant",
      "sortTitle": "transplant",
      "seasonCount": 1,
      "status": "continuing",
      "overview": "The series tells the story of an ER doctor who fled his native Syria to come to Canada, where he must overcome numerous obstacles to resume a career in the high stakes world of emergency medicine.",
      "network": "CTV",
      "airTime": "21:00",
      "images": [
        {
          "coverType": "fanart",
          "url": "https://artworks.thetvdb.com/banners/series/372581/backgrounds/62096147.jpg"
        },
        {
          "coverType": "banner",
          "url": "https://artworks.thetvdb.com/banners/series/372581/banners/62097225.jpg"
        },
        {
          "coverType": "poster",
          "url": "https://artworks.thetvdb.com/banners/series/372581/posters/62073570.jpg"
        }
      ],
      "seasons": [{ "seasonNumber": 1, "monitored": True }],
      "year": 2020,
      "path": "/tv/Transplant",
      "profileId": 1,
      "seasonFolder": True,
      "monitored": True,
      "useSceneNumbering": False,
      "runtime": 45,
      "tvdbId": 372581,
      "tvRageId": 0,
      "tvMazeId": 43828,
      "firstAired": "2020-02-26T00:00:00Z",
      "lastInfoSync": "2020-05-09T19:35:04.359382Z",
      "seriesType": "standard",
      "cleanTitle": "transplant",
      "imdbId": "tt10936342",
      "titleSlug": "transplant",
      "certification": "TV-14",
      "genres": ["Drama"],
      "tags": [],
      "added": "2020-04-06T19:51:03.78814Z",
      "ratings": { "votes": 0, "value": 0.0 },
      "qualityProfileId": 1,
      "id": 47
    },
    "episode": {
      "seriesId": 47,
      "episodeFileId": 0,
      "seasonNumber": 1,
      "episodeNumber": 9,
      "title": "Under Pressure",
      "airDate": "2020-04-29",
      "airDateUtc": "2020-04-30T01:00:00Z",
      "overview": "Bash provides medical care to a friend who is reluctant about treatment, while Mags has her hands full with a young woman who seems to be withholding information. Dr. Bishop offers Mags an incredible opportunity.",
      "hasFile": False,
      "monitored": True,
      "unverifiedSceneNumbering": False,
      "id": 3858
    },
    "quality": {
      "quality": {
        "id": 4,
        "name": "HDTV-720p",
        "source": "television",
        "resolution": 720
      },
      "revision": { "version": 1, "real": 0 }
    },
    "size": 775809144.0,
    "title": "Transplant.S01E09.720p.HDTV.x264-TWERK",
    "sizeleft": 0.0,
    "timeleft": "00:00:00",
    "estimatedCompletionTime": "2020-05-09T21:44:45.646529Z",
    "status": "Completed",
    "trackedDownloadStatus": "Warning",
    "statusMessages": [
      {
        "title": "Transplant.S01E09.720p.HDTV.x264-TWERK",
        "messages": [
          "No files found are eligible for import in /downloads/Transplant.S01E09.720p.HDTV.x264-TWERK"
        ]
      }
    ],
    "downloadId": "57B89B256D23D2C38AD9E680D6DC6163836AD98A",
    "protocol": "torrent",
    "id": 759726777
  }
]
```
