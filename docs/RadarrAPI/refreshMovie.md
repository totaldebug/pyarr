---
layout: default
title: refreshMovie
parent: RadarrAPI
nav_order: 4
---

## Summary

Refresh movie information from TMDb and rescan disk

## Parameters

Required: None

Optional: `movieId (int)` - if not set all movies will be refreshed and scanned

## Example

```python
refreshMovie()
```

## Returns JsonArray

```json
{
    'name': 'RefreshMovie', 
    'body': {
        'sendUpdatesToClient': True, 
        'updateScheduledTask': True, 
        'completionMessage': 'Completed', 
        'name': 'RefreshMovie', 
        'trigger': 'manual'
    }, 
    'priority': 'normal', 
    'status': 'started', 
    'queued': '2020-04-29T08:36:10.742081Z', 
    'started': '2020-04-29T08:36:10.805347Z', 
    'trigger': 'manual', 
    'state': 'started', 
    'manual': True, 
    'startedOn': '2020-04-29T08:36:10.742081Z', 
    'stateChangeTime': '2020-04-29T08:36:10.805347Z', 
    'sendUpdatesToClient': True, 
    'updateScheduledTask': True, 
    'id': 1638638
}
```
