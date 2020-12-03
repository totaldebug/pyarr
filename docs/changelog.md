---
layout: default
title: ChangeLog
nav_order: 7
---

# v1.0.0

- Moved fully to requests from urllib
- Functions changed to snake_case

### Radarr Changes
- Radarr API Renamed to `RadarrApiv1`
- Added the new Radarr API v3 `RadarrAPIv3`

# v0.9.4

### Sonarr New Features

- More robust addSeries
- API Calls
  - setCommand
    - Options Available: RefreshSeries, RescanSeries, EpisodeSearch, SeasonSearch, SeriesSearch, DownloadedEpisodesScan, RssSync, RenameFiles, RenameSeries, Backup, missingEpisodeSearch
  - updSeries
  - updEpisode
  - del_episode_file_by_episode_id

### Radarr New Features

- More robust addMovie
- API Calls
  - setCommand
    - Options Available: RefreshMovie, RescanMovie, MoviesSearch, DownloadedMoviesScan, RssSync, RenameFiles, RenameMovie, CutOffUnmetMoviesSearch, NetImportSync, missingMoviesSearch
  - updMovie

# v0.9.3

- Fixed formatting issues

# v0.9.2

### Radarr Bug Fix

- API Calls
  - getMovie

# v0.9.1

### Radarr New Features

- API Calls
  - delMovie

# v0.9.0

### Sonarr New Features

- API Calls
  - getWanted
  - getLogs
  - getSeries
  - delSeries
  - getBackups
  - delQueue

# v0.8.0

- Updated docs

### Radarr New Features

- API Calls
  - getQueue
  - delQueue
  - getQualityProfiles
  - getHistory

### Sonarr New Features

- API Calls
  - getEpisodesBySeriesId
  - getEpisodeByEpisodeId
  - LookupSeries
  - getRoot
  - addSeries
  - getSystemStatus
  - getQueue
  - delQueue
  - getQualityProfiles
  - getHistory

# v0.7.0

### Radarr New Features

- API Calls
  - getSystemStatus

# v0.6.0

- Documentation Added
- Uploaded to PyPi

### Radarr New Features

- API Calls
  - getCalendar
  - getRoot
  - addMovie
  - getMovie
  - getDiskSpace
  - lookupMovie
  - refreshMovie
  - rescanMovie
  - getCommand
