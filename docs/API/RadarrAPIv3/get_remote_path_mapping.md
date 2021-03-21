---
layout: default
title: get_remote_path_mapping
parent: RadarrAPIv3
nav_order: 4
---

## Summary

Get a list of remote paths being mapped and used by Radarr

## Parameters

Required: None

Optional: None

## Example

```python
get_remote_path_mapping()
```

## Returns JsonArray

```json
[
  {
    "host": "localhost",
    "remotePath": "B:\\",
    "localPath": "A:\\Movies\\",
    "id": 1
  },
  {
    "host": "localhost",
    "remotePath": "C:\\",
    "localPath": "A:\\Movies\\",
    "id": 2
  }
]
```
