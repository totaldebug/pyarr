---
layout: default
title: movieFile
parent: RadarrAPIv3
nav_order: 4
---

# get_movie_file

## Summary

Get a movie file object by its database id.

## Parameters

Required:

- `id (int)` - Database ID for Movie

Optional:

- None


## Example

```python
get_movie_file(588)
```

## Returns JsonArray

```json

```

# del_movie_file

## Summary

Deletes a movie file object by its database id.

## Parameters

Required:
    - `id (int)` = Database ID for movie

Optional:
   - none

## Example

```python
del_movie_file(588)
```

## Returns JsonArray

```json
{}
```
