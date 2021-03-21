---
layout: default
title: get_calendar
parent: SonarrAPI
nav_order: 4
---

## Summary

Gets upcoming episodes, if start/end are not supplied episodes airing today and tomorrow will be returned

## Parameters

Required: None

Optional: `start (date) end (date)`

## Example

```python
get_calendar()
```

```python
get_calendar('2020-01-01', '2020-01-30')
```

## Returns JsonArray
