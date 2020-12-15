---
layout: default
title: history
parent: RadarrAPIv3
nav_order: 4
---

# get_history

## Summary

Return a json object list of items in your history

## Parameters

Required:

- `page (int)` - Default: 1
- `pageSize (int)` - Default: 20
- `sortKey (string)` - Default: date
- `sortDir (string)` - Default: descending

Optional:

- None

## Example

```python
get_history()
```
```python
get_history(2,20,"date","ascending")
```

## Returns JsonArray

```json

```

# get_history_movie

## Summary

Return a json object list of items in your history for the specified movie

## Parameters

Required:
    - `id (int)` = Database ID for movie

Optional:
   - `eventType (int)` = History event type to retrieve

## Example

```python
get_hostory_movie(588)
```
```python
get_hostory_movie(588, 1)
```

## Returns JsonArray

```json
{}
```
