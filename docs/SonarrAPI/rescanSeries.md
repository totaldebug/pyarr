---
layout: default
title: rescanMovie
parent: RadarrAPI
nav_order: 4
---

## Summary

Refresh rescan disk for a single series

## Parameters

Required: None

Optional: `seriesId (int)` - if not set all series will be scanned

## Example

```python
rescanSeries()
```

## Returns JsonArray

```json
{
    'name': 'RescanSeries', 
    'body': {
        'sendUpdatesToClient': True, 
        'updateScheduledTask': True, 
        'completionMessage': 'Completed', 
        'name': 'RescanSeries', 
        'trigger': 'manual'
    }, 
    'priority': 'normal', 
    'status': 'queued', 
    'queued': '2020-04-29T19:02:23.926955Z', 
    'trigger': 'manual', 
    'state': 'queued', 
    'manual': True, 
    'startedOn': '2020-04-29T19:02:23.926955Z', 
    'sendUpdatesToClient': True, 
    'updateScheduledTask': True, 
    'id': 2658453
}
```
