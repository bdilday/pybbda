===============
Getting Started
===============

-------------
Installation
-------------

This package is available on PyPI, so you can install it with 
``pip``, 


.. code-block:: bash

   pip install -U pybbda

Or you can install the latest master branch 
directly from the github repo using
``pip``,


.. code-block:: bash

   pip install git+https://github.com/bdilday/pybbda.git


or download the source,

.. code-block:: bash

   git clone git@github.com:bdilday/pybbda.git
   cd pybbda   
   pip install .


~~~~~~~~~~~~~
Requirements
~~~~~~~~~~~~~

This package explicitly 
supports ``Python 3.6`` and ``Python 3.7``. It aims
to support ``Python 3.8`` but this is not guaranteed.
It explicitly *does not* support any versions 
prior to ``Python 3.6``, including ``Python 2.7``.


---------------------
Environment variables
---------------------

The package uses the following environment variables

* ``PYBBDA_DATA_ROOT``

The root directory for storing data 
(See [Installing data](#Installing-data)). Defaults to ``${INSTALLATION_ROOT}/data/assets``
where ``${INSTALLATION_ROOT}`` is the path the the ``pybbda`` installation.
The code location is typically a path to the ``Python`` installation
plus ``site-packages/pybbda``.

This can cause a problem with write permissions 
if you're using a system `Python` instead of a user-controlled
`virtual environment`_.
For this reason, and to avoid duplication if the package is 
installed into multiple virtual environments, it's 
recommended to use a custom path for ``PYBBDA_DATA_ROOT``, for example,

.. code-block:: bash

   export PYBBDA_DATA_ROOT=${HOME}/.pybbda/data


* ``PYBBDA_LOG_LEVEL``

This sets the `logging level`_ for the package at runtime.
The default is ``INFO``.

---------------
Installing data
---------------

This package ships without any data. Instead it provides tools 
to fetch and store data from a variety of sources. To install
data you can use the ``update`` tool in the ``pybbda.data.tools``
sub-module. 

Example, 

.. code-block:: bash

   python -m pybbda.data.tools.update -h
   
   usage: update.py [-h] [--data-root DATA_ROOT] --data-source
                 {Lahman,BaseballReference,Fangraphs,retrosheet,all}
                 [--make-dirs] [--overwrite] [--create-event-database]
                 [--min-year MIN_YEAR] [--max-year MAX_YEAR]
                 [--num-threads NUM_THREADS]

   optional arguments:
      -h, --help            show this help message and exit
      --data-root DATA_ROOT
                           Root directory for data storage
      --data-source {Lahman,BaseballReference,Fangraphs,retrosheet,all}
                           Update source
      --make-dirs           Make root dir if does not exist
      --overwrite           Overwrite files if they exist
      --create-event-database
                           Create a sqlite database for retrosheet event files
      --min-year MIN_YEAR   Min year to download
      --max-year MAX_YEAR   Max year to download
      --num-threads NUM_THREADS
                           Number of threads to use for downloads



The data will be downloaded to ``--data-root``, which defaults to the
``PYBBDA_DATA_ROOT``. 
By default the script will expect the target directory 
to exist and raise a ``ValueError`` and exit if it does not. 
You can create it or pass option ``--make-dirs`` to update to create it automatically.

The ``--create-event-database`` will cause a ``sqlite`` database to be created in the 
directory ``retrosheet``, under the ``--data-root`` directory.

The ``min-year`` and ``max-year`` arguments refer to Fangraphs leaderboards and to the ``retrosheet`` 
events database, if enabled.

Following are some examples of specific data sources

~~~~~~~~~~~~~
Lahman
~~~~~~~~~~~~~

.. code-block:: bash

   python -m pybbda.data.tools.update --data-source Lahman

.. code-block:: bash

   python -m pybbda.data.tools.update --data-source Lahman --data-root /tmp/missing --make-dirs

~~~~~~~~~~~~~~~~~~~~~~~
Baseball Reference WAR
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
   
   python -m pybbda.data.tools.update --data-source BaseballReference


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fangraphs GUTs and leaderboards
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   python -m pybbda.data.tools.update --data-source Fangraphs

Note that because downloading the full set of
leaderboard data starting from 1871 takes 5-10 minutes, 
by default the years downloaded are 2018 - 2019 only. To get them all
use ``--min-year 1871``

.. code-block:: bash

   python -m pybbda.data.tools.update --data-source Fangraphs --min-year 1871


~~~~~~~~~~~~~~~~~~~~~~~
Retrosheet events
~~~~~~~~~~~~~~~~~~~~~~~

Retrosheet event data is accessed with the pychadwick_ package. 

To store a local copy,

.. code-block:: bash

   $ python -m pybbda.data.tools.update --data-source retrosheet

The ``pychadwick`` package provides a command line tool to parse retrosheet events data as CSV. 
The following downloads the events data to ``/tmp/retrosheet-example`` and then parse them to CSV

.. code-block:: bash

   $ python -m pybbda.data.tools.update --data-source retrosheet --data-root /tmp/retrosheet-example --make-dirs
   INFO:pybbda.data.sources.retrosheet._update:_update:downloading file from https://github.com/chadwickbureau/retrosheet/archive/master.zip

   $ pycwevent --data-root /tmp/retrosheet-example/retrosheet/retrosheet-master/event/regular > /tmp/all_events.csv

The argument ``--create-event-database`` will cause a ``sqlite`` database to be created. Inserting data
takes much longer than bulk uploading a csv, however, this is provided as a convenience. 
The ``min-year`` and ``--max-year`` arguments will limit the years to populate the database with.

.. code-block:: bash

   $ python -m pybbda.data.tools.update --data-source retrosheet --data-root /tmp/retrosheet-example --make-dirs --min-year 1982 --max-year 1982 --create-event-database
   INFO:pybbda.data.sources.retrosheet._update:_update:path /tmp/retrosheet-example/retrosheet/retrosheet-master exists, not downloading
   INFO:pybbda.data.sources.retrosheet._update:_update:creating database with 26 files

.. code-block:: bash
   
   $ ls /tmp/retrosheet-example/retrosheet/
   retrosheet.db  retrosheet-master
   
   $ sqlite3 
   SQLite version 3.11.0 2016-02-15 17:29:24
   Enter ".help" for usage hints.
   Connected to a transient in-memory database.
   Use ".open FILENAME" to reopen on a persistent database.
   sqlite> .open /tmp/retrosheet-example/retrosheet/retrosheet.db
   sqlite> select GAME_ID, BAT_ID, EVENT_CD from event limit 2;
   CIN198204050|willb101|23
   CIN198204050|bowal001|2
   sqlite> .q


~~~~~~~~~~~~~
All sources
~~~~~~~~~~~~~

The argument ``--data-source all`` is a shortcut to downloaded data from 
all the supported sources.

.. code-block:: bash

    python -m pybbda.data.tools.update --data-source all


.. _pychadwick: https://github.com/bdilday/pychadwick
.. _logging level: https://docs.python.org/3.7/library/logging.html
.. _virtual environment: https://docs.python.org/3.7/library/venv.html
