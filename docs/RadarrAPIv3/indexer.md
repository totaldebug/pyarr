---
layout: default
title: history
parent: RadarrAPIv3
nav_order: 4
---

# get_indexer

## Summary

Return a json object list of  indexers, or specify an ID to return a single indexer

## Parameters

Required:

- None

Optional:

- `id (int)` the database id of the indexer

## Example

```python
get_indexer()
```
```python
get_indexer(2)
```

## Returns JsonArray

```json

```

# put_indexer

## Summary

To be looked into, there isnt much documentation on this option


# del_indexer

## Summary

Deleted the indexer based on the database id

## Parameters

Required:
- `id (int)` the database id of the indexer

Optional:
- None
## Example

```python
del_indexer()
```
## Returns JsonArray

```json
[]
```
