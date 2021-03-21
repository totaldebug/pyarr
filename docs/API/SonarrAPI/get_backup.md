---
layout: default
title: get_backup
parent: SonarrAPI
nav_order: 4
---

## Summary

Returns the list of available backups

## Parameters

### Required:

None

### Optional:

None

## Example

```python
get_backup()
```

## Returns JsonArray

```json
[
  {
    "name": "nzbdrone_backup_2017.08.17_22.00.00.zip",
    "path": "/backup/update/nzbdrone_backup_2017.08.17_22.00.00.zip",
    "type": "update",
    "time": "2017-08-18T05:00:37Z",
    "id": 1207435784
  }
]
```
