---
layout: default
title: get_calendar
parent: RadarrAPIv1
nav_order: 4
---

## Summary

Gets upcoming movies, if start/end are not supplied movies airing today and tomorrow will be returned

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
