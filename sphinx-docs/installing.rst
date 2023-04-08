************
Installation
************

Install the package (or add it to your ``requirements.txt`` file):

.. code:: shell

    poetry add pyarr

.. code:: shell

    pip install pyarr

from source:

.. code:: shell

    pip install -e https://github.com/totaldebug/pyarr.git#egg=pyarr

add this to requirements.txt:

.. code:: shell

    -e git+https://github.com/totaldebug/pyarr.git#egg=pyarr


Via Git or Download
===================

#. Go to `Pyarr Repo <https://github.com/totaldebug/pyarr>`
#. Download a copy to your project folders
#. Import as below

.. code:: python

    from pyarr import SonarrAPI
    from pyarr import RadarrAPI
    from pyarr import ReadarrAPI
    from pyarr import LidarrAPI
