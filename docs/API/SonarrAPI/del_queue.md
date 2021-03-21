---
layout: default
title: del_queue
parent: SonarrAPI
nav_order: 4
---

## Summary - NOT TESTED

Deletes an item from the queue and download client. Optionally blacklist item after deletion.

## Parameters

Required:

- `id (int)` Unique ID of the command

Optional:

- `blacklist (bool)` Set to 'true' to blacklist after delete

## Example

```python
del_queue(473989688)
```

```python
del_queue(473989688, True)
```
