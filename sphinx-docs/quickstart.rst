.. _quickstart:

**************
🚀 Quick Start
**************

This quick start guide will take you through the easiest way to get up and running.

Installation
############

This package is distributed on PyPI and can be installed with `pip`:

.. code-block:: shell
   :linenos:
    pip install pyarr


To use the package in your Python project, you will need to import the required modules from below:

.. code-block:: python
   :linenos:

    from pyarr import SonarrAPI
    from pyarr import RadarrAPI
    from pyarr import ReadarrAPI
    from pyarr import LidarrAPI

All of the library modules are based on the same format the below example can be
modified for each one by changing the `sonarr` referances to the required `arr` API:

.. code-block:: python
   :linenos:
    # Import SonarrAPI Class
    from pyarr import SonarrAPI

    # Set Host URL and API-Key
    host_url = 'http://your-domain.com'

    # You can find your API key in Settings > General.
    api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    # Instantiate SonarrAPI Object
    sonarr = SonarrAPI(host_url, api_key)

    # Get and print TV Shows
    print(sonarr.get_series())
