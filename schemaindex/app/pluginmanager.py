from __future__ import unicode_literals
# according to http://python-future.org/compatible_idioms.html#unicode-text-string-literals
#
#
# #import atexit
import os
import shutil
import logging
import json
import time
import importlib
from builtins import str


from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy import create_engine
from sqlalchemy.orm import create_session


from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.fields import *


from .config import cfg, SchemaIndexPluginError
from .dbmodels import MColumn, MTable, MDatasource, MPlugin, Base
from .schemaindexapp import si_app




class PluginManager:
    """ One utility class with functions to deal with all the plugins
    """

    MODEL_DATAFRAME_DIR = 'data'
    MODEL_INSTANCE_DIR = 'instance'
    MODEL_SPEC_DIR = 'plugin' # Save the specs of a specific model, including file mining_model.json
    MODEL_SPEC_PATH = 'plugin' # Save all model_spec programs. One plugin may serve multiple models
    MODEL_SPEC_FILENAME = 'mining_model.json'
    TIME_FORMATER = "%Y-%m-%d %H:%M:%S"

    config = cfg
    schemaindex_home = cfg['main']['schemaflex_home']
    logger = logging.getLogger('stanmo_logger')

    si_db_engine = create_engine('sqlite:///' + cfg['database']['sqlite_file'])
    db_session = create_session(bind=si_db_engine)

    def __init__(self):
        # Add the plugin (model specs) home to sys path for dynamic loading all model specs defined under $STANMO_HOME/plugin
        # sys.path.append(os.path.join(self.schemaindex_home, self.MODEL_SPEC_PATH))

        # self.pluginmanager_init()
        #
        #self.datasource_init() # Calling here cause troubles to __import__, weird. 20171222
        self.si_app = si_app
        self.logger.debug('SchemaIndex plugin manager is started.')


    def pluginmanager_initial_loading(self):

            self.logger.debug('scanning plugins for re-initialization... ')
            self.scan_reflect_plugins()
            self.logger.debug('init error: ' + str(e))  # will not print anything



    def datasource_init(self):

        self.logger.debug('SchemaIndex is trying to boot up all init service by each data source ...')
        ds_list = si_app.get_data_source_rs()

        # Here we loop through all data sources. For each of them, if it is not cached, then it is the first time to run schemaindexapp.
        # We do 2 things for each data source
        # 1. cache the ds_dict
        # 2. run datasource_init of each datasource as defined by plugin.
        for row in ds_list:
            if row.ds_name not in si_app.data_source_dict.keys() :
                si_app.data_source_dict[row.ds_name] = si_app.get_data_source_dict(ds_name=row.ds_name)

                the_engine = self.get_reflect_plugin(p_plugin_name=row.ds_type)['reflect_engine']
                one_ds = the_engine.ReflectEngine(ds_dict = row.to_dict())
                one_ds.datasource_init()

    def get_reflect_plugin(self, p_plugin_name = None):
        p = self.db_session.query(MPlugin).filter_by(plugin_name=p_plugin_name).first()
        return self.load_reflect_engine(p.module_name)

    '''
        def list_reflect_plugins(self):
            logger = si_app.logger # logging.getLogger('stanmo_logger')
    
            return spec_list
    '''

    def scan_reflect_plugins(self):

        self.logger.debug('scanning plugins for re-initialization... ')

        plugin_spec_path = os.path.join(self.schemaindex_home, self.MODEL_SPEC_PATH)

        self.logger.debug('looking for model plugin in path: ' + plugin_spec_path)
        spec_list = []

        for item in os.listdir(plugin_spec_path):
            if os.path.isdir(os.path.join(plugin_spec_path, item)):
                # to avoid : schemaindex.app.config.SchemaIndexPluginError: module '__pycache__' has no attribute 'plugin_name'
                if (item == '__pycache__'):
                    continue
                a_plugin = self.load_reflect_engine(item, plugin_spec_path=plugin_spec_path)
                spec_list.append(a_plugin)


        self.db_session.begin()
        self.db_session.query(MPlugin).delete()
        for plugin_dict in spec_list:
            if plugin_dict is not None:
                self.db_session.add_all([
                    MPlugin( plugin_name=plugin_dict['plugin_name'] ,
                                      module_name=plugin_dict['module_name'] ,
                                      plugin_spec_path=plugin_dict['plugin_spec_path'],
                                      metadata_type = plugin_dict['metadata_type'],
                                      ds_param=json.dumps(plugin_dict['ds_param']),
                                      supported_ds_types=plugin_dict['supported_ds_types'],
                                      notebook_template_path=plugin_dict['notebook_template_path'],
                                      # sample_ds_url=plugin_dict['sample_ds_url'],
                                      author=plugin_dict['author'],
                                      plugin_desc=plugin_dict['plugin_desc'],
                                    )
                                    ])
        self.db_session.commit()



    def load_reflect_engine(self, dottedpath, plugin_spec_path = None):

        assert dottedpath is not None, "dottedpath must not be None"

        try:
            module = __import__(dottedpath, globals(), locals(), [])
            return {'reflect_engine': module,
                    'module_name': dottedpath,
                    'plugin_name': getattr(module, 'plugin_name'),
                    'metadata_type': getattr(module, 'metadata_type'),
                    'ds_param': getattr(module, 'ds_param'),
                    'plugin_spec_path': plugin_spec_path,
                    'notebook_template_path': getattr(module, 'notebook_template_path'),
                    # 'sample_ds_url': getattr(module, 'sample_ds_url'),
                    'plugin_desc': getattr(module, 'plugin_desc'),
                    'supported_ds_types': json.dumps(getattr(module, 'supported_ds_types')) ,
                    'author': getattr(module, 'author'),
                    }
        except Exception as e:
            self.logger.error( "load_reflect_engine (error): Failed to import plugin %s, due to error :{%s}" % (dottedpath, e) )
            # return None
            raise SchemaIndexPluginError(e)



    def reflect_db(self,data_source_name=None):
        session = self.db_session
        dbrs = session.query(MDatasource).filter_by(ds_name=data_source_name)
        for row in dbrs:
            the_engine= self.get_reflect_plugin(row.ds_type)['reflect_engine']
            a_ds = the_engine.ReflectEngine(ds_dict = si_app.get_data_source_dict(ds_name= row.ds_name) ) #SQLAlchemyReflectEngine()
            a_ds.reflect(reload_flag=True)

            session_update = create_session(bind=self.si_db_engine)
            session_update.begin()
            session_update.query(MDatasource).filter_by(ds_name=row.ds_name).\
                update({'last_reflect_date': func.now()}, synchronize_session='fetch')
            session_update.commit()
            session_update.close()
        session.close()

    def generate_notebook_for_table(self, table_id = None, ds_name = None):

        ds_dict = si_app.get_data_source_dict(ds_name= ds_name)
        the_engine = self.get_reflect_plugin(ds_dict['ds_type'])['reflect_engine']

        a_ds = the_engine.ReflectEngine(ds_dict = ds_dict )
        generate_notebook_loc = a_ds.generate_notebook(schemaindex_notebooks_dir=self.config['main']['schemaindex_notebooks']
                               , table_id= table_id)
        return  generate_notebook_loc

    def generate_notebook_snippet_for_table(self, table_id = None, ds_name = None):

        ds_dict = si_app.get_data_source_dict(ds_name= ds_name)
        if ds_dict is None:
            return None
        the_engine = self.get_reflect_plugin(ds_dict['ds_type'])['reflect_engine']
        the_ds = the_engine.ReflectEngine(ds_dict = ds_dict )
        generate_notebook_snippet = the_ds.generate_notebook_snippet(table_id= table_id)
        return  generate_notebook_snippet


si_pm = PluginManager()
