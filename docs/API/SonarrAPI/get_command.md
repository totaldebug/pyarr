---
layout: default
title: get_command
parent: SonarrAPI
nav_order: 4
---

## Summary

Queries the status of a previously started command, or all currently started commands.

## Parameters

Required: None

Optional: `id (int) Unique ID of the Command`

## Example

```python
get_command()
```

```python
get_command(1638308)
```

## Returns JsonArray

```json
{
    'name': 'RefreshSeries',
    'message': 'Completed',
    'body': {
        'sendUpdatesToClient': True,
        'updateScheduledTask': True,
        'completionMessage': 'Completed',
        'name': 'RefreshSeries',
        'trigger': 'manual'
    },
    'priority': 'normal',
    'status': 'completed',
    'queued': '2020-04-28T13:14:19.852449Z',
    'started': '2020-04-28T13:14:19.908555Z',
    'ended': '2020-04-28T13:16:30.590828Z',
    'duration': '00:02:10.6822730',
    'trigger': 'manual',
    'state': 'completed',
    'manual': True,
    'startedOn': '2020-04-28T13:14:19.852449Z',
    'stateChangeTime': '2020-04-28T13:14:19.908555Z',
    'sendUpdatesToClient': True,
    'updateScheduledTask': True,
    'id': 2655615
}
```
