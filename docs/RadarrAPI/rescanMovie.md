---
layout: default
title: rescanMovie
parent: RadarrAPI
nav_order: 4
---

## Summary

Rescan disk for movies

## Parameters

Required: None

Optional: `movieId (int)` - if not set all movies will be scanned

## Example

```python
rescanMovie()
```

## Returns JsonArray

```json
{
    'name': 'RescanMovie', 
    'body': {
        'sendUpdatesToClient': True, 
        'updateScheduledTask': True, 
        'completionMessage': 'Completed', 
        'name': 'RescanMovie', 
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
