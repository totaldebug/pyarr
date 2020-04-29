---
layout: default
title: addMovie
parent: RadarrAPI
nav_order: 4
---

## Summary

Adds a new movie to your collection

## Parameters

Required: 
- dbid = Either, IMDB or TMDB id 
- qualityProfileId = Quailty Profle ID

Optional: 
- None

## Example

```python
addMovie('tt3778644', 1)
```

## Returns JsonArray

```json
{
    'title': 'Solo: A Star Wars Story', 
    'alternativeTitles': [], 
    'secondaryYearSourceId': 0, 
    'sortTitle': 'solo star wars story', 
    'sizeOnDisk': 0, 
    'status': 'tba', 
    'images': [
        {
            'coverType': 'poster', 
            'url': '/MediaCover/243/poster.jpg'
        }
    ], 
    'downloaded': False, 
    'year': 2018, 
    'hasFile': False, 
    'path': '/movies/Solo: A Star Wars Story', 
    'profileId': 1, 
    'pathState': 'static', 
    'monitored': True, 
    'minimumAvailability': 'tba', 
    'isAvailable': True, 
    'folderName': '/movies/Solo: A Star Wars Story', 
    'runtime': 0, 
    'cleanTitle': 'solostarwarsstory', 
    'tmdbId': 348350, 
    'titleSlug': 'solo-a-star-wars-story-348350', 
    'genres': [], 
    'tags': [], 
    'added': '2020-04-29T09:28:54.179226Z', 
    'addOptions': {
        'searchForMovie': True, 
        'ignoreEpisodesWithFiles': False, 
        'ignoreEpisodesWithoutFiles': False
    }, 
    'qualityProfileId': 1, 
    'id': 243
}
```
