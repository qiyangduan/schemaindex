
Overview
============
SchemaIndex is designed for data scientists to find data more efficiently. It can index the tables
and files known to the user.

With schemaindex, you can:
1. Create a data source (e.g. Mysql, Oracle, etc) by registering its connection information.
2. Reflect the data source and index the metadata.
3. Search for all tables/entities in those data sources by their names.

Supported Data Sources
-------------
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
To initialize the schemaindex server, please run this command to load currently available plugins.
This need to be done right after installation only once:

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


*runserver* command should boot up a webserver and open a browser for you.
In the brower, click "datasources" and then click "create ..." to register your own data source.
For example, to register a new HDFS data source, you can input information like the following screenshot:

.. image:: doc/pic/create_data_source.jpg

The next step is to reflect the data source and extract all metadata.
You can do so by clicking button "Relfect Now!" to extract the metadata of the data source,
 or check the box "Reflect Data Source Immediately" during data source creation.

If all previous two steps are successful, you should be able to search the files in "search" box
 appearing in "overview" and "search" page, like the following screenshot: