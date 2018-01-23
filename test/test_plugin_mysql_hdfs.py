from __future__ import unicode_literals
from __future__ import print_function

#
import pytest

from schemaindex.app.config import cfg

from schemaindex.app.schemaindexapp import si_app
from schemaindex.app.pluginmanager import si_pm
import os

@pytest.fixture(scope='module')
def resource_a_setup(request):
    print('\nDoing setup by putting init file')
    db_file_path = cfg['database']['sqlite_file']

    # open(config['main']['init_indicator_file'], 'a').close()
    if os.path.exists(db_file_path):
        print('DB file is ready,  going to delete it .')
        os.remove(db_file_path)


    si_app.schemaindex_init(db_file_path = db_file_path)

    def fin():
        print ("\nDoing teardown")
    request.addfinalizer(fin)



ds_dict = {
    'ds_name': 'emp1',
    'ds_type': 'sqlalchemy',
    'ds_desc': 'created by unittest',
    'ds_param': {'connect_string': 'sqlite:////home/duan/schemaindex.sqlite3.goodbackup',
                 'schema_name': 'na',
                 }
}

def test_plugin_loading(resource_a_setup):
    list1 = si_app.get_plugin_name_list()
    print(list1)
    assert len(list1) == 0

    si_pm.scan_reflect_plugins()

    list1 = si_app.get_plugin_name_list()
    assert  'simplehdfsindex'  in list1



def test_plugin_mysql_add(resource_a_setup):
    dict1 = si_app.get_data_source_dict(ds_name=ds_dict['ds_name'])
    assert dict1 is None

    si_app.add_data_soruce(ds_dict)
    dict1 = si_app.get_data_source_dict(ds_name=ds_dict['ds_name'])
    assert dict1['ds_param']['connect_string'] == ds_dict['ds_param']['connect_string']

def test_plugin_mysql_reflect(after='test_plugin_mysql_add'):

    si_pm.reflect_db(data_source_name=ds_dict['ds_name'])
    suggest1=si_app.get_whoosh_search_suggestion(q='mta')
    print(suggest1)

    assert 'mtable' in suggest1



hdfs_ds_dict = {
    'ds_name': 'hdfs1',
    'ds_type': 'hdfsindex',
    'ds_desc': 'created by unittest of hdfsindex',
    'ds_url': 'http://localhost:50070',
    'ds_param': {'hdfs_web_url': 'http://localhost:50070',
                 'hdfs_url': 'hdfs://localhost:9000',
                 'start_inotify': 'off',
                 'root_path':'/',
                 'inotify_trx_id':'-1',
                 }
}


def test_plugin_hdfs_add():
    dict1 = si_app.get_data_source_dict(ds_name=hdfs_ds_dict['ds_name'])
    assert dict1 is None

    si_app.add_data_soruce(hdfs_ds_dict)
    dict1 = si_app.get_data_source_dict(ds_name=hdfs_ds_dict['ds_name'])
    assert dict1['ds_param']['hdfs_web_url'] ==  'http://localhost:50070'


def test_plugin_hdfs_reflect(after='test_plugin_hdfs_add_reflect'):
    si_pm.reflect_db(data_source_name=hdfs_ds_dict['ds_name'])
    suggest1 = si_app.get_whoosh_search_suggestion(q='citi')
    print(suggest1)
    assert 'cities' in suggest1
    #assert 'dept_name' in suggest1
