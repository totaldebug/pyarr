---
layout: default
title: getQualityProfiles
parent: SonarrAPI
nav_order: 4
---

## Summary

Gets all quality profiles

## Parameters

Required: None

Optional: None

## Example

```python
getQualityProfiles()
```

## Returns JsonArray

```json
[
  {
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
  {
    "name": "HD 720p",
    "cutoff": {
      "id": 4,
      "name": "HDTV-720p"
    },
    "items": [
      {
        "quality": {
          "id": 1,
          "name": "SDTV"
        },
        "allowed": false
      },
      {
        "quality": {
          "id": 8,
          "name": "WEBDL-480p"
        },
        "allowed": false
      },
      {
        "quality": {
          "id": 2,
          "name": "DVD"
        },
        "allowed": false
      },
      {
        "quality": {
          "id": 4,
          "name": "HDTV-720p"
        },
        "allowed": true
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
        "allowed": true
      },
      {
        "quality": {
          "id": 6,
          "name": "Bluray-720p"
        },
        "allowed": true
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
    "id": 2
  },
  {
    "name": "HD 1080p",
    "cutoff": {
      "id": 9,
      "name": "HDTV-1080p"
    },
    "items": [
      {
        "quality": {
          "id": 1,
          "name": "SDTV"
        },
        "allowed": false
      },
      {
        "quality": {
          "id": 8,
          "name": "WEBDL-480p"
        },
        "allowed": false
      },
      {
        "quality": {
          "id": 2,
          "name": "DVD"
        },
        "allowed": false
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
        "allowed": true
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
        "allowed": true
      },
      {
        "quality": {
          "id": 7,
          "name": "Bluray-1080p"
        },
        "allowed": true
      }
    ],
    "id": 3
  },
  {
    "name": "HD - All",
    "cutoff": {
      "id": 4,
      "name": "HDTV-720p"
    },
    "items": [
      {
        "quality": {
          "id": 1,
          "name": "SDTV"
        },
        "allowed": false
      },
      {
        "quality": {
          "id": 8,
          "name": "WEBDL-480p"
        },
        "allowed": false
      },
      {
        "quality": {
          "id": 2,
          "name": "DVD"
        },
        "allowed": false
      },
      {
        "quality": {
          "id": 4,
          "name": "HDTV-720p"
        },
        "allowed": true
      },
      {
        "quality": {
          "id": 9,
          "name": "HDTV-1080p"
        },
        "allowed": true
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
        "allowed": true
      },
      {
        "quality": {
          "id": 6,
          "name": "Bluray-720p"
        },
        "allowed": true
      },
      {
        "quality": {
          "id": 3,
          "name": "WEBDL-1080p"
        },
        "allowed": true
      },
      {
        "quality": {
          "id": 7,
          "name": "Bluray-1080p"
        },
        "allowed": true
      }
    ],
    "id": 4
  }
]
```
