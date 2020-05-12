---
layout: default
title: getLogs
parent: SonarrAPI
nav_order: 4
---

## Summary

Gets a list of all logs

## Parameters

### Required:

None

### Optional:

                optional - sortKey (str) - What key to sort on - Default: 'time'.
                optional - filterKey (str) - What key to filter on - Default: None.
                optional - filterValue (str) - What to filter on (Warn, Info, Error, All) - Default: All.

`page (int)` - 1-indexed
`pageSize (int)` - Default: 10
`sortKey (str)` - Default: time
`filterKey (str)` - Default: None
`filterValue (str)` - (Warn, Info, Error, All) Default: All
`sortDir (string)` - asc or desc - Default: asc

## Example

```python
getLogs()
```

```python
getLogs(sortKey="time", page=1, pageSize=50, filterValue="Error", sortDir="desc")
```

## Returns JsonArray

```json

```
