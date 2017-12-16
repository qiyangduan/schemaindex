from config import cfg
import os
import shutil
import time
import logging
import json
import sys
import dbmodels

# from util import SQLAlchemyReflectEngine
from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy.orm import create_session


from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.fields import *



class SchemaIndexApp:
    """ The runtime platform for running all mining models
    """

    MODEL_DATAFRAME_DIR = 'data'
    MODEL_INSTANCE_DIR = 'instance'
    MODEL_SPEC_DIR = 'spec' # Save the specs of a specific model, including file mining_model.json
    MODEL_SPEC_PATH = 'spec' # Save all model_spec programs. One spec may serve multiple models
    MODEL_SPEC_FILENAME = 'mining_model.json'
    TIME_FORMATER = "%Y-%m-%d %H:%M:%S"

    db_session = create_session(bind=dbmodels.engine)
    logger = logging.getLogger('stanmo_logger')
    indexdir = cfg['main']['schemaflex_text_index_path']
    ix = None
    index_writer = None
    def __init__(self):
        self.stanmo_home = cfg['main']['schemaflex_home']
        self.config = cfg
        # Add the plugin (model specs) home to sys path for dynamic loading all model specs defined under $STANMO_HOME/spec
        sys.path.append(os.path.join(self.stanmo_home, self.MODEL_SPEC_PATH))
        self.schemaindex_init()
        #
        self.logger.debug('SchemaIndex platform is started.')

        #print('openning index')
        #self.ix = index.open_dir(self.indexdir)
        #self.index_writer = self.ix.writer()

    def __del__(self):
        if self.index_writer is not None:
            # print('closing index')
            self.index_writer.cancel()
            self.ix.close() #


    def schemaindex_init(self):
        # import os.path
        to_init_indicator =   cfg['main']['init_indicator_file']


        if not os.path.exists(to_init_indicator):
            return;

        self.logger.debug('SchemaIndex platform is being initialized.') # will not print anything

        os.remove(to_init_indicator)
        # os.remove(textidx)

        db_file_path = os.path.join(os.getcwd(), cfg['database']['sqlite_file'])
        if os.path.exists(db_file_path):
            os.remove(db_file_path)
            # if(False):
        try:
            # recreate the sqlite database file
            engine = dbmodels.create_engine('sqlite:///' + db_file_path)
            self.logger.debug('creating db at ...:  ' + db_file_path) # will not print anything
            dbmodels.Base.metadata.create_all(engine)


            self.logger.debug('scanning plugins ... ')  # will not print anything
            self.scan_reflect_plugins()
        except Exception as e:
            print(str(e))

        self.logger.debug('re-construct text index at folder: ' + self.indexdir)  # will not print anything
        if os.path.exists(db_file_path):
            shutil.rmtree(self.indexdir)
        os.mkdir(self.indexdir)

        schema = Schema(ds_name=ID(stored=True), table_id=ID(stored=True), table_info=TEXT(stored=True)) # , column_info=TEXT(stored=True)
        ix = index.create_in(self.indexdir , schema)
        print("schemaindex: Initialized." )  # will not print anything

    def delete_data_soruce(self,ds_dict = None):
        session = create_session(bind=dbmodels.engine)
        session._model_changes={}

        tab_result = session.query(dbmodels.MTable).filter_by(ds_name=ds_dict['ds_name'])
        if tab_result.count() > 0 and (not ds_dict['delete_reflected_database_automatic'] == 'on'):
            return {'message_type': 'danger',
                    'message_title': 'Error',
                    'message_body':'the data source "' + ds_dict['ds_name'] + '" contains metadata. Please check " Delete Contents in Data Source" and try again'}

        session.begin()
        session.query(dbmodels.MDatasource).filter_by(ds_name=ds_dict['ds_name']).delete(synchronize_session=False)
        session.commit()
        return {'message_type': 'info',
                'message_title': 'Info',
                'message_body': 'the data source "' + ds_dict['ds_name'] + '" is deleted.'}

    def add_data_soruce(self,ds_dict = None):
        session = create_session(bind=dbmodels.engine)
        session._model_changes={}
        try:
            session.begin()
            session.add_all([
                dbmodels.MDatasource(table_group_name=ds_dict['table_group_name'] ,
                                   ds_name=ds_dict['ds_name'] ,
                                   ds_type=ds_dict['ds_type'] ,
                                   ds_url= ds_dict['ds_url'],
                                   nbr_of_tables=0,
                                   nbr_of_columns=9,
                                   ds_desc = 'list of db',
                                   created_date = func.now(),
                        )
            ])
            session.commit()
            dbrs1 = session.query(dbmodels.MDatasource).filter_by(ds_name=ds_dict['ds_name'])
            db = dbrs1.first()
            if db is None:
                si_app.logger.error('error: did not find database')
            return db
        except Exception as e:
            si_app.logger.error('failed to add data source!')
            si_app.logger.error(e)
            return None

    def update_data_soruce(self,ds_dict = None):
        session = create_session(bind=dbmodels.engine)
        session._model_changes={}

        session.begin()
        # db1 = dbmodels.MDatasource.query.filter_by(ds_name=ds_dict['ds_name']).first()
        session.query(dbmodels.MDatasource).filter_by(ds_name=ds_dict['ds_name']).\
            update({'table_group_name': ds_dict['table_group_name'],
                    'ds_type': ds_dict['ds_type'],
                    'ds_url': ds_dict['ds_url'],
                    'ds_desc':ds_dict['ds_desc']})

        #db1.ds_desc = 'list of db updated'
        #db1.ds_url = ds_dict['ds_url']
        session.commit()
        dbrs1 = session.query(dbmodels.MDatasource).filter_by(ds_name=ds_dict['ds_name'])
        db = dbrs1.first()
        if db is None:
            print('error: did not find database')
        return db



    def get_data_source_name_list(self):

        rs = self.db_session.query(dbmodels.MDatasource) #.filter_by(name='ed')

        ds_list = []
        for row in rs:
            ds_list.append({'name': row.ds_name , 'url': row.ds_url } )
        return  ds_list

    def global_whoosh_search(self, q = ''):

        ix = index.open_dir(self.indexdir)
        res = []
        with ix.searcher() as searcher:
            query = QueryParser("table_info", ix.schema).parse(q)
            results = searcher.search(query)
            for r in results:
                res.append({'ds_name': r['ds_name'],
                            'docnum': r.docnum,
                            'table_info': r['table_info'],
                            })

        return res

    def global_whoosh_search_by_id(self, q_id = ''):

        ix = index.open_dir(self.indexdir)
        res = []
        with ix.searcher() as searcher:
            query = QueryParser("table_id", ix.schema).parse(q_id)
            results = searcher.search(query)
            for r in results:
                res.append({'ds_name': r['ds_name'],
                            'docnum': r.docnum,
                            'table_info': r['table_info'],
                            })

        return res

    def delete_doc_from_index_by_docnum(self, p_docnum = None):

        ix = index.open_dir(self.indexdir)
        index_writer = ix.writer()

        index_writer.delete_document(docnum = p_docnum)
        index_writer.commit()
        return True

    def delete_doc_from_index_by_datasource(self, ds_name = None):

        ix = index.open_dir(self.indexdir)
        index_writer = ix.writer()

        ix = index.open_dir(self.indexdir)
        res = []
        with ix.searcher() as searcher:
            query = QueryParser("ds_name", ix.schema).parse(ds_name)
            num = index_writer.delete_by_query(q=query)
            si_app.logger.info( '{0:10} documents from data source {1:15}  '.format( str(num), ds_name) )

        index_writer.commit()
        return True



    def get_whoosh_search_suggestion(self, q = ''):

        indexdir = self.indexdir
        ix = index.open_dir(indexdir)

        res = []
        with ix.reader() as r:
            # print (r.most_frequent_terms("table_info", number=5, prefix='dep'))
            for aterm in r.most_frequent_terms("table_info", number=5, prefix=q):
                res.append(aterm[1]) # The result was like (1.0, 'dept_manager'), but here i need only a keyword
                print (aterm)

        return res


    def add_table_content_index(self,ds_name = None, table_id = None, table_info = None):

        ix = index.open_dir(self.indexdir)
        index_writer = ix.writer()
        index_writer.add_document(ds_name = unicode(ds_name), table_id=unicode(table_id), table_info=unicode(table_info))
        index_writer.commit()

    def commit_index(self, table_id=None, table_info=None):
        return
        self.index_writer.commit()
        self.ix = index.open_dir(self.indexdir)
        self.index_writer = self.ix.writer()



    def get_data_source_rs(self):

        rs = self.db_session.query(dbmodels.MDatasource).order_by(dbmodels.MDatasource.ds_name.asc()) #.filter_by(name='ed')
        return rs

    def get_data_source_dict(self, ds_name = None):

        rs = self.db_session.query(dbmodels.MDatasource).filter_by(ds_name=ds_name)
        if rs.count() > 0:
            ds = rs.first()
            return {x.name: getattr(ds, x.name) for x in ds.__table__.columns}

            ''''{
                'ds_name': ds.ds_name,
                'ds_url': ds.ds_url,
                'db_trx_id': ds.db_trx_id,
                'ds_type': ds.ds_type,
                'table_group_name': ds.table_group_name,
            }'''
        return None

    def get_plugin_name_list(self):
        plugins = []
        rs =  self.db_session.query(dbmodels.MPlugin)
        for p in rs:
            plugins.append(p.plugin_name)
        return  plugins

    def get_plugin_list(self):
        plugins = []
        rs = self.db_session.query(dbmodels.MPlugin)
        for p in rs:
            plugins.append(p)
        return  plugins

    def get_plugin_info(self, p_plugin_name = ''):

        p = self.db_session.query(dbmodels.MPlugin).filter_by(plugin_name=p_plugin_name).first()
        p['ds_param'] = json.loads(p['ds_param'])
        return  p


    def get_reflect_plugin(self, p_plugin_name = None):
        p = self.db_session.query(dbmodels.MPlugin).filter_by(plugin_name=p_plugin_name).first()
        return self.load_reflect_engine(p.module_name)


    def get_table_list_for_data_source_rs(self, param_ds_name = ''):
        sql = '''
                SELECT c.ds_name,  c.table_name, t.table_comment, group_concat(c.column_name)   as column_names
                FROM mcolumn c, mtable t
                where c.table_name = t.table_name and c.ds_name = t.ds_name and t.ds_name = \'''' + param_ds_name + '''\'
                GROUP BY c.ds_name, c.table_name;
                '''

        tabrs = dbmodels.engine.execute(sql)
        return  tabrs


    def reflect_db(self,data_source_name=None):
        session = create_session(bind=dbmodels.engine)
        dbrs = session.query(dbmodels.MDatasource).filter_by(ds_name=data_source_name)
        for row in dbrs:
                the_engine= si_app.get_reflect_plugin(row.ds_type)['reflect_engine']
                a_ds = the_engine.ReflectEngine(ds_dict = self.get_data_source_dict(ds_name= row.ds_name) ) #SQLAlchemyReflectEngine()
                a_ds.reflect(reload_flag=True)


    def list_data_sources(self):
        model_list = []
        models = []

        session = create_session(bind=dbmodels.engine)
        dbrs = session.query(dbmodels.MDatasource)  # .filter_by(name='ed')


        for db in dbrs:
                models.append(db)
        if len(models) > 0:
            print('{0:20}   {1:20}  {2:35}  '.format('data source name',
                                                                           'data source type',
                                                                           'URL'
                                                                           ))
            for a_model in models:
                print('{0:20}   {db_type_name:20}  {table_group_name:35}  '.format(a_model.ds_name,
                                                                          db_type_name=a_model.ds_type,
                                                                          table_group_name = a_model.ds_url
                                                                                           )
                      )
        else:
            print('No data source is found!')

        logging.getLogger('stanmo_logger').debug('discovered models: ' + model_list.__str__())
        return model_list


    def list_reflect_plugins(self):
        logger = logging.getLogger('stanmo_logger')
        logger.debug('looking for reflect engine from location: ' + os.path.join(self.stanmo_home, self.MODEL_SPEC_PATH) )
        plugin_spec_path = os.path.join(self.stanmo_home, self.MODEL_SPEC_PATH)
        logger = logging.getLogger('stanmo_logger')
        logger.debug('looking for model spec in path: ' + plugin_spec_path)
        spec_list = []

        for item in os.listdir(plugin_spec_path):
            if os.path.isdir(os.path.join(plugin_spec_path, item)):
                a_plugin = self.load_reflect_engine(item,plugin_spec_path = plugin_spec_path)
                spec_list.append(a_plugin)
        return spec_list

    def scan_reflect_plugins(self):
        plist = self.list_reflect_plugins()

        self.db_session.begin()
        self.db_session.query(dbmodels.MPlugin).delete()
        for plugin_dict in plist:
            if plugin_dict is not None:
                self.db_session.add_all([
                    dbmodels.MPlugin( plugin_name=plugin_dict['plugin_name'] ,
                                      module_name=plugin_dict['module_name'] ,
                                      plugin_spec_path=plugin_dict['plugin_spec_path'],
                                      ds_param=json.dumps(plugin_dict['ds_param']),
                                      supported_ds_types=plugin_dict['supported_ds_types'],
                                      notebook_template_path=plugin_dict['notebook_template_path'],
                                      sample_ds_url=plugin_dict['sample_ds_url'],
                                      author=plugin_dict['author'],
                                      plugin_desc=plugin_dict['plugin_desc'],
                                    )
                                    ])
        self.db_session.commit()



    def load_reflect_engine(self, dottedpath, plugin_spec_path = None):

        assert dottedpath is not None, "dottedpath must not be None"
        #splitted_path = dottedpath.split('.')
        #modulename = '.'.join(splitted_path[:-1])
        #classname = splitted_path[-1]
        # print(sys.path)


        try:
            module = __import__(dottedpath, globals(), locals(), [])
            return {'reflect_engine': module,
                    'module_name': dottedpath,
                    'plugin_name': getattr(module, 'plugin_name'),
                    'ds_param': getattr(module, 'ds_param'),
                    'plugin_spec_path': plugin_spec_path,
                    'notebook_template_path': getattr(module, 'notebook_template_path'),
                    'sample_ds_url': getattr(module, 'sample_ds_url'),
                    'plugin_desc': getattr(module, 'plugin_desc'),
                    'supported_ds_types': json.dumps(getattr(module, 'supported_ds_types')) ,
                    'author': getattr(module, 'author'),
                    }
        except Exception as e:
            self.logger.error( "load_reflect_engine (error): Failed to import plugin %s, due to error :{%s}" % (dottedpath, e) )

            return None


si_app = SchemaIndexApp()
