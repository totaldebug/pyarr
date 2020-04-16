Sonarr and Radarr API Python Wrapper
==========================

Forked from [SLiX69/Sonarr-API-Python-Wrapper](https://github.com/SLiX69/Sonarr-API-Python-Wrapper)

Unofficial Python Wrapper for the [Sonarr](https://github.com/Sonarr/Sonarr) and [Radarr](https://github.com/Radarr/Radarr) API. We currently only support Sonarr and have not tested for Radarr. 

### Requirements
- requests

### Example Usage:

```
# Import SonarrAPI Class
from arr import SonarrAPI

# Set Host URL and API-Key
host_url = 'http://your-domain.com/api'

# You can find your API key in Settings > General.
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Instantiate SonarrAPI Object
sonarr = SonarrAPI(host_url, api_key)

# Get and print TV Shows
print sonarr.get_series()
```

### Documentation

[Sonarr API Documentation](https://github.com/Sonarr/Sonarr/wiki/API)
