---
layout: default
title: delMovie
parent: RadarrAPI
nav_order: 4
---

## Summary

Delete the movie with the given ID

## Parameters

Required:

- `id (int)` Movie ID from Radarr

Optional:

- `delFiles (bool)`  if true the movie folder and all files will be deleted when the movie is deleted
- `addException (bool)` if true the movie TMDBID will be added to the import exclusions list when the movie is deleted

## Example

```python
delMovie(1)
```

## Returns JsonArray

```json
{}
```
