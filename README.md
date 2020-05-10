# Sonarr and Radarr API Python Wrapper

Original Sonarr wrapper from [SLiX69/Sonarr-API-Python-Wrapper](https://github.com/SLiX69/Sonarr-API-Python-Wrapper) which has been mostly re-written and Radarr added by myself.

Unofficial Python Wrapper for the [Sonarr](https://github.com/Sonarr/Sonarr) and [Radarr](https://github.com/Radarr/Radarr) API.

Currently the package is under development, see the full [documentation](https://marksie1988.github.io/PyArr) for supported commands

### Requirements

- requests

### Example Sonarr Usage:

```
# Import SonarrAPI Class
from PyArr import SonarrAPI

# Set Host URL and API-Key
host_url = 'http://your-domain.com'

# You can find your API key in Settings > General.
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Instantiate SonarrAPI Object
sonarr = SonarrAPI(host_url, api_key)

# Get and print TV Shows
print(sonarr.getSeries())
```

### Example Radarr Usage:

```
# Import RadarrAPI Class
from PyArr import RadarrAPI

# Set Host URL and API-Key
host_url = 'http://your-domain.com'

# You can find your API key in Settings > General.
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Instantiate RadarrAPI Object
radarr = RadarrAPI(host_url, api_key)

# Get and print TV Shows
print(radarr.getCalendar())
```

### Documentation

- [PyArr Documentation](https://docs.totaldebug.uk/PyArr)
- [Sonarr API Documentation](https://github.com/Sonarr/Sonarr/wiki/API)
- [Radarr API Documentation](https://github.com/Radarr/Radarr/wiki/API)
