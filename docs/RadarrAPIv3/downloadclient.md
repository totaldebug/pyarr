---
layout: default
title: downloadclient
parent: RadarrAPIv3
nav_order: 4
---

# get_downloadclient

## Summary

Return a json object list of  downloadclient, or specify an ID to return a single downloadclient

## Parameters

Required:

- None

Optional:

- `id (int)` the database id of the downloadclient

## Example

```python
get_downloadclient()
```
```python
get_downloadclient(2)
```

## Returns JsonArray

```json

```

# put_downloadclient

## Summary

To be looked into, there isnt much documentation on this option


# del_downloadclient

## Summary

Deleted the downloadclient based on the database id

## Parameters

Required:
- `id (int)` the database id of the downloadclient

Optional:
- None
## Example

```python
del_downloadclient(2)
```
## Returns JsonArray

```json
[]
```
