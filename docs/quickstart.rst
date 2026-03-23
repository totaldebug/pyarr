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

Synchronous Usage
-----------------

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

Asynchronous Usage
------------------

.. code-block:: python
   :linenos:

    import asyncio
    # Import AsyncSonarr Class
    from pyarr import AsyncSonarr

    async def main():
        # Set Host, API-Key and Port
        host = 'your-domain.com'
        api_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        port = 8989

        # Instantiate AsyncSonarr Object
        async with AsyncSonarr(host, api_key, port) as sonarr:
            # Get and print TV Shows using the series component
            print(await sonarr.series.get())

    asyncio.run(main())

Advanced Configuration
######################

PyArr supports several advanced configuration options to make it easier to integrate with other systems like Home Assistant.

Full URL Support
----------------

You can now pass a full URL as the ``host`` parameter. PyArr will automatically extract the scheme, host, port, and subpath:

.. code-block:: python
   :linenos:

    # All of these are valid ways to instantiate a client
    sonarr = Sonarr("http://192.168.1.100:8989/sonarr", api_key)
    sonarr = Sonarr("localhost", api_key, port=8989, tls=False)

Custom Sessions
---------------

If you are using PyArr in an environment that manages its own HTTP sessions (like Home Assistant), you can pass an existing ``httpx.AsyncClient`` (for async) or ``httpx.Client`` (for sync):

.. code-block:: python
   :linenos:

    import httpx
    from pyarr import AsyncSonarr

    async with httpx.AsyncClient() as session:
        async with AsyncSonarr(host, api_key, session=session) as sonarr:
            print(await sonarr.series.get())

SSL Verification and Custom Headers
-----------------------------------

You can disable SSL verification (useful for self-signed certificates) and provide custom headers:

.. code-block:: python
   :linenos:

    sonarr = Sonarr(
        host,
        api_key,
        verify_ssl=False,
        headers={"User-Agent": "MyCustomApp/1.0"}
    )

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
