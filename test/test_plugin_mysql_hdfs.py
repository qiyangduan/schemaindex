from __future__ import print_function

#
import pytest

from schemaindex.app.schemaindexapp import si_app

from schemaindex.app.config import  cfg as config



@pytest.fixture(scope='module')
def resource_a_setup(request):
    print('\nDoing setup by putting init file')
    open(config['main']['init_indicator_file'], 'a').close()
    si_app.schemaindex_init()

    def fin():
        print ("\nDoing teardown")
    request.addfinalizer(fin)

ds_dict = {
    'ds_name': 'emp1',
    'ds_type': 'sqlalchemy',
    'ds_desc': 'created by unittest of hdfsindex',
    'ds_param': {'connect_string': 'mysql://root:ttt@localhost/employees',
                 'schema_name': 'na',
                 }
}



def test_plugin_mysql_add(resource_a_setup):
    dict1 = si_app.get_data_source_dict(ds_name=ds_dict['ds_name'])
    assert dict1 is None

    si_app.add_data_soruce(ds_dict)
    dict1 = si_app.get_data_source_dict(ds_name=ds_dict['ds_name'])
    assert dict1['ds_param']['connect_string'] == 'mysql://root:learning@localhost/employees'


def test_plugin_mysql_reflect(after='test_plugin_mysql_add'):

    si_app.reflect_db(data_source_name=ds_dict['ds_name'])
    suggest1=si_app.get_whoosh_search_suggestion(q='dept')
    print(suggest1)

    assert 'dept_no' in suggest1
    assert 'dept_name' in suggest1



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
    si_app.reflect_db(data_source_name=hdfs_ds_dict['ds_name'])
    suggest1 = si_app.get_whoosh_search_suggestion(q='cities')
    print(suggest1)
    assert 'cities.csv' in suggest1
    #assert 'dept_name' in suggest1
