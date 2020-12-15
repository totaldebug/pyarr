# Sonarr and Radarr API Python Wrapper

Unofficial Python Wrapper for the [Sonarr](https://github.com/Sonarr/Sonarr) and [Radarr](https://github.com/Radarr/Radarr) API.

Now supports Radarr v3 API


Based on the origional wrapper from [SLiX69/Sonarr-API-Python-Wrapper](https://github.com/SLiX69/Sonarr-API-Python-Wrapper).

See the full [documentation](https://docs.totaldebug.uk/pyarr/) for supported functions.

### Requirements

- requests

### Example Sonarr Usage:

```
# Import SonarrAPI Class
from pyarr import SonarrAPI

# Set Host URL and API-Key
host_url = 'http://your-domain.com'

# You can find your API key in Settings > General.
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Instantiate SonarrAPI Object
sonarr = SonarrAPI(host_url, api_key)

# Get and print TV Shows
print(sonarr.getSeries())
```

### Example Radarr API v1 Usage:

```
# Import RadarrAPI Class
from pyarr import RadarrAPIv1

# Set Host URL and API-Key
host_url = 'http://your-domain.com'

# You can find your API key in Settings > General.
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Instantiate RadarrAPI Object
radarr = RadarrAPIv1(host_url, api_key)

# Get and print TV Shows
print(radarr.getCalendar())
```

### Documentation

- [pyarr Documentation](https://docs.totaldebug.uk/pyarr)
- [Sonarr API Documentation](https://github.com/Sonarr/Sonarr/wiki/API)
- [Radarr v1 API Documentation](https://github.com/Radarr/Radarr/wiki/API)
- [Radarr v3 API Documentation](https://radarr.video/docs/api)
