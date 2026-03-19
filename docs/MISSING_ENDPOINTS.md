# Missing API Endpoints in PyArr

This document lists the API endpoints from the "Arr" suite that are currently missing or not fully implemented in the new `pyarr` structure. This list is based on the official OpenAPI specifications and documentation for each service.

## Common Components (Shared across most services)

The following endpoints are available in most services but may not be fully exposed in `pyarr`:

- **Config Management**:
  - `GET/PUT /api/v3/config/host`: General host settings (port, API key, etc.).
  - `GET/PUT /api/v3/config/naming`: File and folder naming formats.
  - `GET/PUT /api/v3/config/ui`: User interface settings.
- **System Operations**:
  - `POST /api/v3/system/backup/restore`: Restore from a backup.
  - `GET /api/v3/system/routes`: List all available API routes.
- **Media Management**:
  - `GET /api/v3/parse`: Parse a title or path to identify media.
  - `GET /api/v3/rename`: List files that need renaming.
  - `POST /api/v3/rename`: Execute renaming operations.

---

## Sonarr Specific

- **Series & Episodes**:
  - `PUT /api/v3/series/editor`: Bulk update multiple series.
  - `POST /api/v3/series/import`: Bulk import series from a path.
  - `POST /api/v3/episode/monitor`: Bulk update episode monitored status.
  - `POST /api/v3/episode/search`: Trigger search for specific episodes.
- **Wanted List**:
  - `GET /api/v3/wanted/cutoff`: List episodes where the quality cutoff is unmet.
- **Profiles**:
  - `GET/POST/PUT/DELETE /api/v3/languageprofile`: Full CRUD for language profiles.
  - `GET/POST/PUT/DELETE /api/v3/delayprofile`: Full CRUD for delay profiles.

---

## Radarr Specific

- **Movies**:
  - `PUT /api/v3/movie/editor`: Bulk update multiple movies.
  - `POST /api/v3/movie/import`: Bulk import movies from a path.
- **Custom Formats**:
  - `GET/POST/PUT/DELETE /api/v3/customformat`: Full CRUD for Custom Formats.
  - `GET /api/v3/customformat/schema`: Get schema for custom formats.
- **Collections**:
  - `GET /api/v3/collection`: List movie collections.
  - `GET /api/v3/collection/{id}`: Get specific collection details.

---

## Lidarr Specific

- **Artists & Albums**:
  - `PUT /api/v1/artist/editor`: Bulk update multiple artists.
  - `PUT /api/v1/album/editor`: Bulk update multiple albums.
- **Media Management**:
  - `GET /api/v1/retag`: List files that need retagging.
  - `POST /api/v1/retag`: Execute retagging operations.
- **Profiles**:
  - `GET/POST/PUT/DELETE /api/v1/metadataprofile`: Full CRUD for metadata profiles.

---

## Prowlarr Specific

- **Indexer Management**:
  - `POST /api/v1/indexer/test`: Test a specific indexer configuration.
  - `POST /api/v1/indexer/testall`: Test all configured indexers.
  - `GET /api/v1/indexerstats`: Performance statistics for indexers.
  - `GET /api/v1/indexerstatus`: Detailed health status for indexers.
- **Sync Management**:
  - `GET/POST/PUT/DELETE /api/v1/appprofile`: Manage application sync profiles.

---

## Bazarr Specific

- **Resource Management**:
  - `GET/POST/PUT/DELETE /api/series`: Manage TV series within Bazarr.
  - `GET/POST/PUT/DELETE /api/movies`: Manage movies within Bazarr.
  - `GET/POST/PUT/DELETE /api/episodes`: Manage episodes within Bazarr.
- **Subtitle Operations**:
  - `GET /api/subtitles/wanted`: List media missing subtitles.
  - `POST /api/subtitles/search`: Trigger search for subtitles.

---

## Dispatcharr Specific

- **Exports**:
  - `GET /epg`: Export XMLTV data.
  - `GET /m3u`: Export M3U playlist data.
- **Management**:
  - `GET/POST/PUT/DELETE /api/v1/series-rules`: Manage DVR/Series recording rules.
