---
layout: default
title: getWanted
parent: SonarrAPI
nav_order: 4
---

## Summary

Gets missing episode (episodes without files)

## Parameters

### Required:

`sortKey (string)` - series.title or airDateUtc default=airDateUtc

### Optional:

`page (int)` - 1-indexed
`pageSize (int)` - Default: 10
`sortDir (string)` - asc or desc - Default: asc

## Example

```python
getWanted()
```

```python
getWanted(sortKey="series.title", page=1, pageSize=50, sortDir="desc")
```

## Returns JsonArray

```json
{
  "page": 1,
  "pageSize": 15,
  "sortKey": "airDateUtc",
  "sortDirection": "descending",
  "totalRecords": 2, //Use to disable paging when additional results are not available
  "records": [
    {
      "seriesId": 1,
      "episodeFileId": 0,
      "seasonNumber": 5,
      "episodeNumber": 4,
      "title": "Archer Vice: House Call",
      "airDate": "2014-02-03",
      "airDateUtc": "2014-02-04T03:00:00Z",
      "overview": "Archer has to stage an intervention for Pam that gets derailed by an unwanted guest. ",
      "hasFile": false,
      "monitored": true,
      "sceneEpisodeNumber": 0,
      "sceneSeasonNumber": 0,
      "tvDbEpisodeId": 0,
      "absoluteEpisodeNumber": 50,
      "series": {
        "tvdbId": 110381,
        "tvRageId": 23354,
        "imdbId": "tt1486217",
        "title": "Archer (2009)",
        "cleanTitle": "archer2009",
        "status": "continuing",
        "overview": "At ISIS, an international spy agency, global crises are merely opportunities for its highly trained employees to confuse, undermine, betray and royally screw each other. At the center of it all is suave master spy Sterling Archer, whose less-than-masculine code name is \"Duchess.\" Archer works with his domineering mother Malory, who is also his boss. Drama revolves around Archer's ex-girlfriend, Agent Lana Kane and her new boyfriend, ISIS comptroller Cyril Figgis, as well as Malory's lovesick secretary, Cheryl.",
        "airTime": "7:00pm",
        "monitored": true,
        "qualityProfileId": 1,
        "seasonFolder": true,
        "lastInfoSync": "2014-02-05T04:39:28.550495Z",
        "runtime": 30,
        "images": [
          {
            "coverType": "banner",
            "url": "http://slurm.trakt.us/images/banners/57.12.jpg"
          },
          {
            "coverType": "poster",
            "url": "http://slurm.trakt.us/images/posters/57.12-300.jpg"
          },
          {
            "coverType": "fanart",
            "url": "http://slurm.trakt.us/images/fanart/57.12.jpg"
          }
        ],
        "seriesType": "standard",
        "network": "FX",
        "useSceneNumbering": false,
        "titleSlug": "archer-2009",
        "path": "E:\\Test\\TV\\Archer (2009)",
        "year": 2009,
        "firstAired": "2009-09-18T02:00:00Z",
        "qualityProfile": {
          "value": {
            "name": "SD",
            "cutoff": {
              "id": 1,
              "name": "SDTV"
            },
            "items": [
              {
                "quality": {
                  "id": 1,
                  "name": "SDTV"
                },
                "allowed": true
              },
              {
                "quality": {
                  "id": 8,
                  "name": "WEBDL-480p"
                },
                "allowed": true
              },
              {
                "quality": {
                  "id": 2,
                  "name": "DVD"
                },
                "allowed": true
              },
              {
                "quality": {
                  "id": 4,
                  "name": "HDTV-720p"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 9,
                  "name": "HDTV-1080p"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 10,
                  "name": "Raw-HD"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 5,
                  "name": "WEBDL-720p"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 6,
                  "name": "Bluray-720p"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 3,
                  "name": "WEBDL-1080p"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 7,
                  "name": "Bluray-1080p"
                },
                "allowed": false
              }
            ],
            "id": 1
          },
          "isLoaded": true
        },
        "seasons": [
          {
            "seasonNumber": 5,
            "monitored": true
          },
          {
            "seasonNumber": 4,
            "monitored": true
          },
          {
            "seasonNumber": 3,
            "monitored": true
          },
          {
            "seasonNumber": 2,
            "monitored": true
          },
          {
            "seasonNumber": 1,
            "monitored": true
          },
          {
            "seasonNumber": 0,
            "monitored": false
          }
        ],
        "id": 1
      },
      "downloading": false,
      "id": 55
    },
    {
      "seriesId": 1,
      "episodeFileId": 0,
      "seasonNumber": 5,
      "episodeNumber": 3,
      "title": "Archer Vice: A Debt of Honor",
      "airDate": "2014-01-27",
      "airDateUtc": "2014-01-28T03:00:00Z",
      "overview": "Pam makes a deal that puts everyone in danger. Archer dons his slightly darker black suit to save the day.",
      "hasFile": false,
      "monitored": true,
      "sceneEpisodeNumber": 0,
      "sceneSeasonNumber": 0,
      "tvDbEpisodeId": 0,
      "absoluteEpisodeNumber": 49,
      "series": {
        "tvdbId": 110381,
        "tvRageId": 23354,
        "imdbId": "tt1486217",
        "title": "Archer (2009)",
        "cleanTitle": "archer2009",
        "status": "continuing",
        "overview": "At ISIS, an international spy agency, global crises are merely opportunities for its highly trained employees to confuse, undermine, betray and royally screw each other. At the center of it all is suave master spy Sterling Archer, whose less-than-masculine code name is \"Duchess.\" Archer works with his domineering mother Malory, who is also his boss. Drama revolves around Archer's ex-girlfriend, Agent Lana Kane and her new boyfriend, ISIS comptroller Cyril Figgis, as well as Malory's lovesick secretary, Cheryl.",
        "airTime": "7:00pm",
        "monitored": true,
        "qualityProfileId": 1,
        "seasonFolder": true,
        "lastInfoSync": "2014-02-05T04:39:28.550495Z",
        "runtime": 30,
        "images": [
          {
            "coverType": "banner",
            "url": "http://slurm.trakt.us/images/banners/57.12.jpg"
          },
          {
            "coverType": "poster",
            "url": "http://slurm.trakt.us/images/posters/57.12-300.jpg"
          },
          {
            "coverType": "fanart",
            "url": "http://slurm.trakt.us/images/fanart/57.12.jpg"
          }
        ],
        "seriesType": "standard",
        "network": "FX",
        "useSceneNumbering": false,
        "titleSlug": "archer-2009",
        "path": "E:\\Test\\TV\\Archer (2009)",
        "year": 2009,
        "firstAired": "2009-09-18T02:00:00Z",
        "qualityProfile": {
          "value": {
            "name": "SD",
            "cutoff": {
              "id": 1,
              "name": "SDTV"
            },
            "items": [
              {
                "quality": {
                  "id": 1,
                  "name": "SDTV"
                },
                "allowed": true
              },
              {
                "quality": {
                  "id": 8,
                  "name": "WEBDL-480p"
                },
                "allowed": true
              },
              {
                "quality": {
                  "id": 2,
                  "name": "DVD"
                },
                "allowed": true
              },
              {
                "quality": {
                  "id": 4,
                  "name": "HDTV-720p"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 9,
                  "name": "HDTV-1080p"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 10,
                  "name": "Raw-HD"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 5,
                  "name": "WEBDL-720p"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 6,
                  "name": "Bluray-720p"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 3,
                  "name": "WEBDL-1080p"
                },
                "allowed": false
              },
              {
                "quality": {
                  "id": 7,
                  "name": "Bluray-1080p"
                },
                "allowed": false
              }
            ],
            "id": 1
          },
          "isLoaded": true
        },
        "seasons": [
          {
            "seasonNumber": 5,
            "monitored": true
          },
          {
            "seasonNumber": 4,
            "monitored": true
          },
          {
            "seasonNumber": 3,
            "monitored": true
          },
          {
            "seasonNumber": 2,
            "monitored": true
          },
          {
            "seasonNumber": 1,
            "monitored": true
          },
          {
            "seasonNumber": 0,
            "monitored": false
          }
        ],
        "id": 1
      },
      "downloading": false,
      "id": 54
    },
  ]
}
```
