---
layout: default
title: delSeries
parent: SonarrAPI
nav_order: 4
---

## Summary

Deletes the series with the specified ID

## Parameters

Required:

- `id (int)` Series ID from Sonarr

Optional:

- `delFiles (bool)`  Delete any files for the series

## Example

```python
delSeries(1)
```

## Returns JsonArray

```json
{}
```
