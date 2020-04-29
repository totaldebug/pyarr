---
layout: default
title: lookupMovie
parent: RadarrAPI
nav_order: 4
---

## Summary

Searches for new movies on trakt

## Parameters

Required: None

Optional: 
- One of the following:
  - `term` = Enter the Movie's Name, using `%20` to signify spaces, as in `term=Star%20Wars`
  - `tmdbId` = `348350`
  - `imdbId` = `tt3778644`

## Example

```python
lookupMovie()
```

```python
lookupMovie('Star%20Wars')
```

```python
lookupMovie('348350')
```

```python
lookupMovie('tt3778644')
```

## Returns JsonArray

```json
{
    'title': 'Solo: A Star Wars Story', 
    'alternativeTitles': [], 
    'secondaryYearSourceId': 0, 
    'sortTitle': 'solo star wars story', 
    'sizeOnDisk': 0, 
    'status': 'released', 
    'overview': 'Through a series of daring escapades deep within a dark and dangerous criminal underworld Han Solo meets his mighty future copilot Chewbacca and encounters the notorious gambler Lando Calrissian.', 
    'inCinemas': '2018-05-15T00:00:00Z', 
    'images': [
        {
            'coverType': 'poster', 
            'url': 'http://image.tmdb.org/t/p/original/4oD6VEccFkorEBTEDXtpLAaz0Rl.jpg'
        }
    ], 
    'downloaded': False, 
    'year': 2018, 
    'hasFile': False, 
    'profileId': 0, 
    'pathState': 'dynamic', 
    'monitored': False, 
    'minimumAvailability': 'tba', 
    'isAvailable': True, 
    'folderName': '', 
    'runtime': 0, 
    'tmdbId': 348350, 
    'titleSlug': 'solo-a-star-wars-story-348350', 
    'genres': [], 
    'tags': [], 
    'added': '0001-01-01T00:00:00Z', 
    'ratings': {
        'votes': 5152, 
        'value': 6.6
    }, 
    'qualityProfileId': 0
}
```
