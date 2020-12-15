---
layout: default
title: notification
parent: RadarrAPIv3
nav_order: 4
---

# get_notification

## Summary

Return a json object list of notifications, or specify an ID to return a single notification

## Parameters

Required:

- None

Optional:

- `id (int)` the database id of the notification

## Example

```python
get_notification()
```
```python
get_notification(2)
```

## Returns JsonArray

```json

```

# put_notification

## Summary

To be looked into, there isnt much documentation on this option


# del_notification

## Summary

Deleted the notification based on the database id

## Parameters

Required:
- `id (int)` the database id of the notification

Optional:
- None
## Example

```python
del_notification(2)
```
## Returns JsonArray

```json
[]
```
