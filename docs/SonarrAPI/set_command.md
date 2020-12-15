---
layout: default
title: set_command
parent: SonarrAPI
nav_order: 4
---

## Summary

Performs any of the predetermined Sonarr command routines.

Options available: RefreshSeries, RescanSeries, EpisodeSearch, SeasonSearch, SeriesSearch, DownloadedEpisodesScan, RssSync, RenameFiles, RenameSeries, Backup, missingEpisodeSearch

## Parameters

Required: name (string)

Optional: Additional parameters may be required or optional. See [https://github.com/Radarr/Radarr/wiki/API:Command](https://github.com/Radarr/Radarr/wiki/API:Command) on a per command basis.

## Example

```python
set_command(name="RescanSeries", seriesId=series_id)
```

## Returns JsonArray

```json
{
  "name": "RescanSeries",
  "body": {
    "sendUpdatesToClient": True,
    "updateScheduledTask": True,
    "completionMessage": "Completed",
    "name": "RescanSeries",
    "trigger": "manual"
  },
  "priority": "normal",
  "status": "queued",
  "queued": "2020-04-29T19:02:23.926955Z",
  "trigger": "manual",
  "state": "queued",
  "manual": True,
  "startedOn": "2020-04-29T19:02:23.926955Z",
  "sendUpdatesToClient": True,
  "updateScheduledTask": True,
  "id": 2658453
}
```
