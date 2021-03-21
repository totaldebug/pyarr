---
layout: default
title: getEpisodesByEpisodeId
parent: SonarrAPI
nav_order: 4
---

## Summary

Returns the episode with the matching id

## Parameters

Required: id (int)

Optional: None

## Example

```python
getEpisodesByEpisodeId(1)
```

## Returns JsonArray

```json
{
  "seriesId": 1,
  "episodeFileId": 0,
  "seasonNumber": 1,
  "episodeNumber": 1,
  "title": "Mole Hunt",
  "airDate": "2009-09-17",
  "airDateUtc": "2009-09-18T02:00:00Z",
  "overview": "Archer is in trouble with his Mother and the Comptroller because his expense account is way out of proportion to his actual expenses. So he creates the idea that a Mole has breached ISIS and he needs to get into the mainframe to hunt him down (so he can cover his tracks!). All this leads to a surprising ending.",
  "hasFile": false,
  "monitored": true,
  "sceneEpisodeNumber": 0,
  "sceneSeasonNumber": 0,
  "tvDbEpisodeId": 0,
  "absoluteEpisodeNumber": 1,
  "downloading": false,
  "id": 1
}
```
