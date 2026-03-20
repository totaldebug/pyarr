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

    from pyarr import Sonarr, Radarr, Readarr, Lidarr, Prowlarr, Bazarr, Whisparr, Dispatcharr

All of the library modules are based on the same format. The below example shows how to use Sonarr:

.. code-block:: python
   :linenos:

    # Import Sonarr Class
    from pyarr import Sonarr

    # Set Host, API-Key and Port
    host = 'your-domain.com'
    api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    port = 8989

    # Instantiate Sonarr Object
    sonarr = Sonarr(host, api_key, port)

    # Get and print TV Shows using the series component
    print(sonarr.series.get())

Composition-based Architecture
##############################

The new version of PyArr uses a composition-based architecture. Instead of a flat list of methods, functionality is grouped into components:

*   ``client.series``: Manage TV series (Sonarr, Bazarr)
*   ``client.movie``: Manage movies (Radarr, Bazarr, Whisparr)
*   ``client.system``: System status, health, and operations
*   ``client.tag``: Manage tags
*   ``client.queue``: Monitor and manage the download queue
*   ``client.history``: View activity history
*   ... and many more.

This structure makes the library more intuitive and easier to maintain.
