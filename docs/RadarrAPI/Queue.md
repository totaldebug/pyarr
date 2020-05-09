---
layout: default
title: Queue
parent: RadarrAPI
nav_order: 4
---

# Get

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
    "movie": {
      "title": "Mowgli",
      "alternativeTitles": [
        {
          "sourceType": "tmdb",
          "movieId": 16,
          "title": "Mowgli",
          "sourceId": 407436,
          "votes": 0,
          "voteCount": 0,
          "language": "english",
          "id": 21
        }
      ],
      "secondaryYearSourceId": 0,
      "sortTitle": "mowgli",
      "sizeOnDisk": 2948099499,
      "status": "released",
      "overview": "Mowgli lives in the jungle. Nice movie.",
      "inCinemas": "2018-11-24T23:00:00Z",
      "physicalRelease": "2018-12-07T00:00:00Z",
      "physicalReleaseNote": "Netflix",
      "images": [
        {
          "coverType": "poster",
          "url": "http://image.tmdb.org/t/p/original/8TSLWaf6yNjjitt52vxycVsufZA.jpg"
        },
        {
          "coverType": "fanart",
          "url": "http://image.tmdb.org/t/p/original/pApaVlxJCp2o4mrzCAD3AaLjq77.jpg"
        }
      ],
      "website": "https://www.netflix.com/title/80993105",
      "downloaded": true,
      "year": 2018,
      "hasFile": true,
      "youTubeTrailerId": "ZZGQ0zftr-w",
      "studio": "The Imaginarium",
      "path": "/storage/movies/Mowgli (2018)",
      "profileId": 4,
      "pathState": "static",
      "monitored": false,
      "minimumAvailability": "released",
      "isAvailable": true,
      "folderName": "/storage/movies/Mowgli (2018)",
      "runtime": 104,
      "lastInfoSync": "2019-08-12T15:34:21.823878Z",
      "cleanTitle": "mowgli",
      "imdbId": "tt2388771",
      "tmdbId": 407436,
      "titleSlug": "mowgli-407436",
      "genres": [],
      "tags": [1],
      "added": "2019-08-12T15:34:18.737789Z",
      "ratings": {
        "votes": 1466,
        "value": 6.6
      },
      "movieFile": {
        "movieId": 0,
        "relativePath": "Mowgli (2018) Web-Dl 1080p x264 AC3-NoTag.mkv",
        "size": 2948099499,
        "dateAdded": "2019-08-16T08:52:55.490036Z",
        "releaseGroup": "NoTag",
        "quality": {
          "quality": {
            "id": 3,
            "name": "WEBDL-1080p",
            "source": "webdl",
            "resolution": "r1080P",
            "modifier": "none"
          },
          "customFormats": [],
          "revision": {
            "version": 1,
            "real": 0
          }
        },
        "edition": "",
        "id": 4
      },
      "qualityProfileId": 4,
      "id": 16
    },
    "quality": {
      "quality": {
        "id": 3,
        "name": "WEBDL-1080p",
        "source": "webdl",
        "resolution": "r1080P",
        "modifier": "none"
      },
      "customFormats": [],
      "revision": {
        "version": 1,
        "real": 0
      }
    },
    "size": 2948099499.0,
    "title": "Mowgli (2018) Web-Dl 1080p x264 AC3-NoTag.mkv",
    "sizeleft": 0.0,
    "timeleft": "00:00:00",
    "estimatedCompletionTime": "2019-08-16T09:10:12.721926Z",
    "status": "Completed",
    "trackedDownloadStatus": "Warning",
    "statusMessages": [
      {
        "title": "Mowgli (2018) Web-Dl 1080p x264 AC3-NoTag.mkv",
        "messages": [
          "No files found are eligible for import in /home/usr/download/movies/Mowgli (2018) Web-Dl 1080p x264 AC3-NoTag.mkv"
        ]
      }
    ],
    "downloadId": "123456789xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "protocol": "torrent",
    "id": 473989688
  }
]
```

# Delete

## Summary

Deletes an item from the queue and download client. Optionally blacklist item after deletion.

## Parameters

Required:

- `id (int)` Unique ID of the command

Optional:

- `blacklist (bool)` Set to 'true' to blacklist after delete

## Example

```python
delQueue(473989688)
```

```python
delQueue(473989688, True)
```
