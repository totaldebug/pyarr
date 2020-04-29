---
layout: default
title: refreshSeries
parent: SonarrAPI
nav_order: 4
---

## Summary

Refresh series information from trakt and rescan disk

## Parameters

Required: None

Optional: `seriesId (int)` - if not set all movies will be refreshed and scanned

## Example

```python
refreshSeries()
```

## Returns JsonArray

```json
{
    'name': 'RefreshSeries', 
    'message': 'Scanning disk for Killing Eve', 
    'body': {
        'sendUpdatesToClient': True, 
        'updateScheduledTask': True, 
        'completionMessage': 'Completed', 
        'name': 'RefreshSeries', 
        'trigger': 'manual'
    }, 
    'priority': 'normal', 
    'status': 'started', 
    'queued': '2020-04-29T18:58:19.168363Z', 
    'started': '2020-04-29T18:58:19.226896Z', 
    'trigger': 'manual', 
    'state': 'started', 
    'manual': True, 
    'startedOn': '2020-04-29T18:58:19.168363Z', 
    'stateChangeTime': '2020-04-29T18:58:19.226896Z', 
    'sendUpdatesToClient': True, 
    'updateScheduledTask': True, 
    'id': 2658444
}
```
