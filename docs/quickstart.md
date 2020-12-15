---
layout: default
title: 🚀 Quick Start With pyarr
nav_order: 1
---

# 🚀 Quick Start With GitHub Pages

## Requirements

- Minimum Radarr ver:
  - v1 API: 0.2.0.1480
  - v3 API: 3.0.0.0
- Minimum Sonarr ver: 2.0.0.5344

## Install with pip

### from package

```shell
pip install PyArr
```

### from source

* Run the following command:

  ```shell
  pip install -e https://github.com/marksie1988/pyarr.git#egg=pyarr
  ```

* Add this to requirements.txt or run a requirements export

  ```shell
  -e git+https://github.com/marksie1988/pyarr.git#egg=pyarr
  ```

## Include with project

* Go to [pyarr Repo](https://github.com/marksie1988/pyarr)
* Download a copy into your project folder
* Import as below:
  ```python
  from pyarr import SonarrAPI
  from pyarr import RadarrAPIv1
  from pyarr import RadarrAPIv3
  ```

## Exanple usage

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
print(sonarr.get_calendar())
```

```python
# Import SonarrAPI Class
from pyarr import RadarrAPIv3

# Set Host URL and API-Key
host_url = 'http://your-domain.com'

# You can find your API key in Settings > General.
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Instantiate RadarrAPI Object
radarr = RadarrAPI(host_url, api_key)

# Get and print TV Shows
print(radarr.get_calendar())
```
