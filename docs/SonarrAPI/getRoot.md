---
layout: default
title: getRoot
parent: SonarrAPI
nav_order: 4
---

## Summary

Queries the status of root folder.

## Parameters

Required: None

Optional: None

## Example

```python
getRoot()
```

## Returns JsonArray

```json
[
  {
    "path": "/tv/",
    "freeSpace": 3843787325440,
    "totalSpace": 5798228656128,
    "id": 3
  }
]
```
