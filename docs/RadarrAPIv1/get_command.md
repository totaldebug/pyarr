---
layout: default
title: get_command
parent: RadarrAPIv1
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
    'name': 'RefreshMovie',
    'message': 'Completed',
    'body': {
        'sendUpdatesToClient': True,
        'updateScheduledTask': True,
        'completionMessage': 'Completed',
        'name': 'RefreshMovie',
        'trigger': 'manual'
    },
    'priority': 'normal',
    'status': 'completed',
    'queued': '2020-04-28T11:15:23.128315Z',
    'started': '2020-04-28T11:15:23.222789Z',
    'ended': '2020-04-28T11:15:50.549924Z',
    'duration': '00:00:27.3271350',
    'trigger': 'manual',
    'state': 'completed',
    'manual': True,
    'startedOn': '2020-04-28T11:15:23.128315Z',
    'stateChangeTime': '2020-04-28T11:15:23.222789Z',
    'sendUpdatesToClient': True,
    'updateScheduledTask': True,
    'id': 1638308
}
```
