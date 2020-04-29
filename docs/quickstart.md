---
layout: default
title: 🚀 Quick Start With PyArr
nav_order: 1
---

# 🚀 Quick Start With GitHub Pages

## Requirements

- Minimum Radarr ver: 0.2.0.1480
- Minimum Sonarr ver: 2.0.0.5344

## Install with pip

### from package

```shell
pip install PyArr
```

### from source

* Run the following command:
  
  ```shell
  pip install -e https://github.com/marksie1988/PyArr.git#egg=PyArr
  ```

* Add this to requirements.txt or run a requirements export
  
  ```shell
  -e git+https://github.com/marksie1988/PyArr.git#egg=PyArr
  ```

## Include with project

* Go to [PyArr Repo](https://github.com/marksie1988/PyArr)
* Download a copy into your project folder
* Import as below:
  ```python
  from PyArr import SonarrAPI
  from PyArr import RadarrAPI
  ```

## Exanple usage

```python
# Import SonarrAPI Class
from PyArr import SonarrAPI

# Set Host URL and API-Key
host_url = 'http://your-domain.com'

# You can find your API key in Settings > General.
api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Instantiate SonarrAPI Object
sonarr = SonarrAPI(host_url, api_key)

# Get and print TV Shows
print(sonarr.getCalendar())
```

```python
# Import SonarrAPI Class
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
