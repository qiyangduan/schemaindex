
====================================

# SchemaIndex
SchemaIndex is designed to index the schemas known to you. You can:
1. register the data sources (e.g. Mysql, Oracle, etc) with its connection information.
2. Search for all tables/entities in those data sources by their names.

# Supported Database Types
* Oracle
* Mysql
* Sqlite



Installation
============

On Linux
-------------
(tested 20171222) Stardard  `pip`_ should be able to install schemaindex:

.. code-block:: bash

    # Make sure we have an up-to-date version of pip and setuptools:
    $ pip install schemaindex


(If ``pip`` installation fails for some reason, you can try
``easy_install httpie`` as a fallback.)

How to use
============

How to start a SchemaIndex Server
-------------
After the installation, at the first time, please run this command to load currently available plugins:

.. code-block:: bash
    $ schemaindex reload plugin

The following is a sample output:

.. code-block:: bash
    (py3env1) duan:py3env1$ schemaindex reload plugin
    Plugins are reloaded.
    Reflect Plugin Name:                     Path:
    hdfsindex                                /home/duan/virenv/py3env1/local/lib/python2.7/site-packages/schemaindex/plugin/hdfsindex
    sqlalchemy                               /home/duan/virenv/py3env1/local/lib/python2.7/site-packages/schemaindex/plugin/sqlalchemyindex

To start the schemaindex server, please run this command:
.. code-block:: bash
    $ schemaindex runserver

The following is a sample output:

.. code-block:: bash
    (py3env1) duan:py3env1$ schemaindex runserver
    Server started, please visit : http://localhost:8088/


Once you installed schemaindex, you can start
