.. raw:: html

   <h1 align="center">


.. raw:: html

   </h1>

   <h1 align="center">

Pyarr: Sonarr and Radarr API Python Wrapper

.. raw:: html

   </h1>

   <p align="center">


.. raw:: html

   </p>

   <p align="center">

.. raw:: html

   </p>

--------------

*****
About
*****

.. raw:: html

   <table>
   <tr>
   <td>

**Pyarr* is a **high-quality** *Python API Wrapper* that provides access to
both Radarr and Sonarr Rest APIs directry from Python.

.. raw:: html

   </td>
   </tr>
   </table>

************
Installation
************

This package is distributed on PyPI_ and can be installed with ``pip``:

.. code:: console

   $ pip install pyarr

To use the package in your Python project, you will need to add the following:

.. code:: python

    from pyarr import SonarrAPI
    from pyarr import RadarrAPI

For more information read the full documentation on `installing the package`_

.. _PyPI: https://pypi.python.org/pypi/pyarr
.. _installing the package: https://docs.totaldebug.uk/pyarr/installing.html

Example Sonarr Usage:
=====================

.. code:: python

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


Example Radarr API Usage:
=========================

.. code:: python

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

************
Contributing
************

Got **something interesting** you'd like to **share**? Learn about
contributing in our `contributing guide`_.

.. _contributing guide: https://docs.totaldebug.uk/pyarr/contributing.html

******
Author
******

.. list-table::
   :header-rows: 1

   * - |TotalDebug|
   * - **marksie1988 (Steven Marks)**


Credits
=======

-  `Archmonger <https://github.com/Archmonger>`__ Some excellent contribution and improvements

*******
Support
*******

Reach out to me at one of the following places:

-  `Discord <https://discord.gg/6fmekudc8Q>`__
-  `Discussions <https://github.com/totaldebug/pyarr/discussions>`__
-  `Issues <https://github.com/totaldebug/pyarr/issues/new/choose>`__

******
Donate
******

Please consider supporting this project by sponsoring, or just donating
a little via `our sponsor
page <https://github.com/sponsors/marksie1988>`__

*******
License
*******

|License: CC BY-NC-SA 4.0|

-  Copyright © `Total Debug <https://totaldebug.uk>`__.

.. |TotalDebug| image:: https://totaldebug.uk/assets/images/logo.png
   :target: https://linkedin.com/in/marksie1988
   :width: 150
.. |License: CC BY-NC-SA 4.0| image:: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-orange.svg?style=flat-square
   :target: https://creativecommons.org/licenses/by-nc-sa/4.0/
