Common Components
=================

These components are shared between clients, but they are **not** available on every
client - each Arr only exposes the ones its API actually answers. Accessing one that a
client does not support raises ``AttributeError``, so a mistake surfaces immediately
rather than as a 404 or, on Bazarr and Dispatcharr, a 200 carrying their web page.

The support below was established by probing live instances.

.. list-table::
    :header-rows: 1
    :widths: 40 60

    * - Component
      - Available on
    * - System
      - Every client
    * - Backup, Command, Download Client, History, Log, Notification, Tag, Update
      - Sonarr, Radarr, Lidarr, Readarr, Whisparr, Prowlarr
    * - Indexer
      - Sonarr, Radarr, Lidarr, Readarr, Whisparr, Prowlarr
    * - Blocklist, Calendar, Import List, Metadata, Quality Definition, Quality Profile,
        Queue, Remote Path Mapping, Root Folder, Wanted
      - Sonarr, Radarr, Lidarr, Readarr, Whisparr
    * - Import List Exclusion
      - Sonarr, Radarr, Lidarr, Readarr, Whisparr
    * - Any of the above not listed for a client
      - Not exposed on that client

Bazarr and Dispatcharr have their own APIs and expose only ``system`` from this set,
alongside their own client specific components.

Backup
------
.. automodule:: pyarr._sync.common.backup
    :members:

Blocklist
---------
.. automodule:: pyarr._sync.common.blocklist
    :members:

Calendar
--------
.. automodule:: pyarr._sync.common.calendar
    :members:

Command
-------
.. automodule:: pyarr._sync.common.command
    :members:

Download Client
---------------
.. automodule:: pyarr._sync.common.download_client
    :members:

History
-------
.. automodule:: pyarr._sync.common.history
    :members:

Import List
-----------
.. automodule:: pyarr._sync.common.import_list
    :members:

Import List Exclusion
---------------------

Available on Radarr, Sonarr, Lidarr, Readarr and Whisparr. Radarr serves the exclusion list
from ``exclusions``, the others from ``importlistexclusion``; the client wires the correct
path for you.

.. automodule:: pyarr._sync.common.import_list_exclusion
    :members:

Indexer
-------
.. automodule:: pyarr._sync.common.indexer
    :members:

Log
---
.. automodule:: pyarr._sync.common.log
    :members:

Metadata
--------
.. automodule:: pyarr._sync.common.metadata
    :members:

Notification
------------
.. automodule:: pyarr._sync.common.notification
    :members:

Quality Definition
------------------
.. automodule:: pyarr._sync.common.quality_definition
    :members:

Quality Profile
---------------
.. automodule:: pyarr._sync.common.quality_profile
    :members:

Queue
-----
.. automodule:: pyarr._sync.common.queue
    :members:

Remote Path Mapping
-------------------
.. automodule:: pyarr._sync.common.remote_path_mapping
    :members:

Root Folder
-----------
.. automodule:: pyarr._sync.common.root_folder
    :members:

System
------
.. automodule:: pyarr._sync.common.system
    :members:

Tag
---
.. automodule:: pyarr._sync.common.tag
    :members:

Update
------
.. automodule:: pyarr._sync.common.update
    :members:
