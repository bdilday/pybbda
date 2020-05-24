============
Installation
============

This package is not available on PyPi but is on github.

You can install directly from the repo using
``pip``,

.. code-block:: bash

   pip install git+https://github.com/bdilday/pybbda.git

or clone the source repo,

.. code-block:: bash

   git clone git@github.com:bdilday/pybbda.git
   cd pybbda
   pip install -e .

------------
Requirements
------------

This package explicitly 
supports ``Python 3.6`` and ``Python 3.7``. It aims
to support ``Python 3.8`` but this is not guaranteed.
It explicitly *does not* support any versions 
prior to ``Python 3.6``, including ``Python 2.7``.

----------------------
Package vs module name
----------------------

In the tradition of ``scikit-learn``, the ``pybbda`` *package*
provides a *module* ``pybaseballdatana``. This means imports work in
the following way,

.. code-block:: python

   from pybaseballdatana.data import LahmanData

This also means the installation directory is ``pybaseballdatana``
and not ``pybbda``.

---------------------
Environment variables
---------------------

The package uses the following environment variables

* ``PYBBDA_DATA_ROOT``

The root directory for storing data 
(See [Installing data](#Installing-data)). Defaults to ``${INSTALLATION_ROOT}/data/assets``
where ``${INSTALLATION_ROOT}`` is the path the the ``pybbda`` installation.
The code location is typically a path to the ``Python`` installation
plus ``site-packages/pybaseballdatana``.

This can cause a problem with write permissions 
if you're using a system `Python` instead of a user-controlled
[virtual environment](https://docs.python.org/3.7/library/venv.html). 
For this reason, and to avoid duplication if the package is 
installed into multiple virtual environments, it's 
recommended to use a custom path for `PYBBDA_DATA_ROOT`, for example,

.. code-block:: bash

   export PYBBDA_DATA_ROOT=${HOME}/.pybbda/data


* ``PYBBDA_LOG_LEVEL``

This sets the [logging level](https://docs.python.org/3.7/library/logging.html) for the package at runtime.
The default is ``INFO``.

---------------
Installing data
---------------

This package ships without any data. Instead it provides tools 
to fetch and store data from a variety of sources. To install
data you can use the ``update`` tool in the ``pybaseballdatana.data.tools``
sub-module. 

Example, 

.. code-block:: bash

   $ python -m pybaseballdatana.data.tools.update -h
   usage: update.py [-h] [--data-root DATA_ROOT] --data-source
                    {Lahman,BaseballReference,Fangraphs,all} [--make-dirs]
                    [--overwrite] [--min-year MIN_YEAR] [--max-year MAX_YEAR]
                    [--num-threads NUM_THREADS]

   optional arguments:
     -h, --help            show this help message and exit
     --data-root DATA_ROOT
                           Root directory for data storage
     --data-source {Lahman,BaseballReference,Fangraphs,all}
                           Update source
     --make-dirs           Make root dir if does not exist
     --overwrite           Overwrite files if they exist
     --min-year MIN_YEAR   Min year to download
     --max-year MAX_YEAR   Max year to download
     --num-threads NUM_THREADS
                           Number of threads to use for downloads


The data will be downloaded to ``--data-root``, which defaults to the
``PYBBDA_DATA_ROOT``

The ``min-year`` and ``max-year`` arguments refer only
to Fangraphs leaderboards as of now. 
