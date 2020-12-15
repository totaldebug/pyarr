---
layout: default
title: importlist
parent: RadarrAPIv3
nav_order: 4
---

# get_importlist

## Summary

Return a json object list of import lists, or specify an ID to return a single import list

## Parameters

Required:

- None

Optional:

- `id (int)` the database id of the import list

## Example

```python
get_importlist()
```
```python
get_importlist(2)
```

## Returns JsonArray

```json

```

# put_importlist

## Summary

To be looked into, there isnt much documentation on this option


# del_importlist

## Summary

Deleted the import list based on the database id

## Parameters

Required:
- `id (int)` the database id of the import list

Optional:
- None
## Example

```python
del_importlist(2)
```
## Returns JsonArray

```json
[]
```
