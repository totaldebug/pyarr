---
layout: default
title: get_disk_space
parent: SonarrAPI
nav_order: 4
---

## Summary

Queries the server disks and returns space information.

---
**NOTE**

This will not return any mounted NFS Shares, only the root disk.

---

## Parameters

Required: None

Optional: None

## Example

```python
get_disk_space()
```

## Returns JsonArray

```json
[
    {
        'path': '/',
        'label': '',
        'freeSpace': 10056593408,
        'totalSpace': 10726932480
    }
]
```
