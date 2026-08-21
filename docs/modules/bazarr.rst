Bazarr
======
.. note::
    An asynchronous version of this client is available as ``AsyncBazarr``.
    The API is identical, but all methods are coroutines and must be awaited.

.. automodule:: pyarr._sync.bazarr
    :members:

Episodes
--------
.. automodule:: pyarr._sync.bazarr.episodes
    :members:

Movies
------
.. automodule:: pyarr._sync.bazarr.movies
    :members:

Providers
---------
.. automodule:: pyarr._sync.bazarr.providers
    :members:

Series
------
.. automodule:: pyarr._sync.bazarr.series
    :members:

Subtitles
---------
.. automodule:: pyarr._sync.bazarr.subtitles
    :members:

Wanted
------

Bazarr has no combined wanted endpoint, so it exposes ``wanted_episodes`` and
``wanted_movies`` rather than a single ``wanted``. Each uses the shared
:class:`pyarr._sync.common.wanted.Wanted` component pointed at the matching path.

.. automodule:: pyarr._sync.common.wanted
    :members:
    :noindex:
