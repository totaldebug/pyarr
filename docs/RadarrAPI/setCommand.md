---
layout: default
title: setCommand
parent: RadarrAPI
nav_order: 4
---

## Summary

Performs any of the predetermined Radarr command routines.

Options available: RefreshMovie, RescanMovie, MoviesSearch, DownloadedMoviesScan, RssSync, RenameFiles, RenameMovie, CutOffUnmetMoviesSearch, NetImportSync, missingMoviesSearch

## Parameters

Required: name (string)

Optional: Additional parameters may be required or optional. See [https://github.com/Radarr/Radarr/wiki/API:Command](https://github.com/Radarr/Radarr/wiki/API:Command) on a per command basis.

## Example

```python
setCommand(name="MoviesSearch", movieIds=movie_id)
```

## Returns JsonArray

```json
{
    'name': 'MoviesSearch', 
    'body': {
        'sendUpdatesToClient': True, 
        'updateScheduledTask': True, 
        'completionMessage': 'Completed', 
        'name': 'MoviesSearch', 
        'trigger': 'manual'
    },   
    'priority': 'normal', 
    'status': 'queued', 
    'queued': '2020-04-29T08:38:17.177166Z', 
    'trigger': 'manual', 
    'state': 'queued', 
    'manual': True, 
    'startedOn': '2020-04-29T08:38:17.177166Z', 
    'sendUpdatesToClient': True, 
    'updateScheduledTask': True, 
    'id': 1638792
}
```
