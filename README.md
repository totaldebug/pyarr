# Sonarr and Radarr API Python Wrapper

Python Wrapper for the [Sonarr](https://github.com/Sonarr/Sonarr) and [Radarr](https://github.com/Radarr/Radarr) API.

See the full [documentation](https://docs.totaldebug.uk/pyarr/) for supported functions.

### Requirements

-   requests

### Example Sonarr Usage:

```python
# Import SonarrAPI Class
from pyarr import SonarrAPI

# Set Host URL and API-Key
host_url = 'http://your-domain.com'

# You can find your API key in Settings > General.
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Instantiate SonarrAPI Object
sonarr = SonarrAPI(host_url, api_key)

# Get and print TV Shows
print(sonarr.get_series(123))
```

### Example Radarr Usage:

```python
# Import RadarrAPI Class
from pyarr import RadarrAPI

# Set Host URL and API-Key
host_url = 'http://your-domain.com'

# You can find your API key in Settings > General.
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Instantiate RadarrAPI Object
radarr = RadarrAPI(host_url, api_key)

# Get and print TV Shows
print(radarr.get_root_folder())
```

### Documentation

-   [Pyarr Documentation](https://docs.totaldebug.uk/pyarr)
-   [Sonarr API Documentation](https://github.com/Sonarr/Sonarr/wiki/API)
-   [Radarr API Documentation](https://radarr.video/docs/api)
