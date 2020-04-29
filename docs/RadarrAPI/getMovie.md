---
layout: default
title: getMovie
parent: RadarrAPI
nav_order: 4
---

## Summary

Work in Progress
{: .label .label-yellow } 

Returns all Movies in your collection

## Parameters

Required: None

Optional: `id(int)` - returns movie with the matching ID

## Example

```python
getMovie()
```

```python
getMovie(1234)
```

## Returns JsonArray

```json
[
    {
        'path': '/', 
        'label': '', 
        'freeSpace': 10056593408, 
        'totalSpace': 10726932480
    }
]
```
