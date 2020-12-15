---
layout: default
title: get_custom_filter
parent: RadarrAPIv3
nav_order: 4
---

## Summary

Query Radarr for custom filters

## Parameters

Required: None

Optional: None

## Example

```python
get_custom_filter()
```

## Returns JsonArray

```json
[
  {
    "type": "movieIndex",
    "label": "Rated G",
    "filters": [
      {
        "key": "certification",
        "value": [
          "G"
        ],
        "type": "equal"
      }
    ],
    "id": 10
  }
]
```
