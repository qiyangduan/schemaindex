import tornado.web
import json
from sqlalchemy.orm import create_session
from sqlalchemy import create_engine



from .dbmodels import MDatasource,MTable,MColumn

from .schemaindexapp import si_app
from .pluginmanager import si_pm
# si_app.datasource_init() # This call was in si_app.__init__, but it failed with "not able to load module". So i moved it here.


engine = create_engine('sqlite:///' + si_app.config['database']['sqlite_file'])


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")




class ReloadPluginHandler(tornado.web.RequestHandler):
    def get(self):
        si_pm.scan_reflect_plugins()
        session = create_session(bind=engine)
        dbrs = si_app.get_data_source_rs()
        ds_count = dbrs.count()

        base_navigation_dict = {'selected_menu': 'overview',
                                'dbrs': dbrs,
                                'plugin_list': si_app.get_plugin_list(),
                                'ds_count':str(ds_count),
                                #'tab_count':str(tab_count),
                                #'attr_count':str(attr_count),
                                #'tag_count':'NA',

        }

        self.render("overview.html", base_navigation_dict=base_navigation_dict)



class OverviewHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        # print('overview ed')
        session = create_session(bind=engine)
        dbrs = si_app.get_data_source_rs()

        ds_count = dbrs.count()
        #tab_count = session.query(MTable).count()
        #attr_count = session.query(MColumn).count()
        base_navigation_dict = {'selected_menu': 'overview',
                                'dbrs': dbrs,
                                'plugin_list': si_app.get_plugin_list(),
                                'ds_count':str(ds_count),
                                #'tab_count':str(tab_count),
                                #'attr_count':str(attr_count),
                                #'tag_count':'NA',

        }

        self.render("overview.html", base_navigation_dict=base_navigation_dict)


class GlobalSearchHandler(tornado.web.RequestHandler):
    def get(self):
        q = ''
        res = []
        dbrs = si_app.get_data_source_rs()

        base_navigation_dict = {'selected_menu': 'search',
                                'dbrs': dbrs,
                                'selected_schema_name': ''
                                }
        self.render("global_search_result.html",
                    dbrs=dbrs,
                    q=q,
                    base_navigation_dict=base_navigation_dict,
                    search_result = res)

    def post(self):

        q = self.get_argument('q')
        res = si_app.global_whoosh_search(q)
        dbrs = si_app.get_data_source_rs()

        base_navigation_dict = {'selected_menu': 'search',
                                'dbrs': dbrs,
                                'selected_schema_name': ''
                                }
        self.render("global_search_result.html",
                    dbrs=dbrs,
                    q=q,
                    base_navigation_dict=base_navigation_dict,
                    search_result = res)


class DatabaseSummaryHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        # param_db_name = self.get_argument("table_group_name", None)
        session = create_session(bind=engine)
        param_ds_name = self.get_argument("ds_name", None)
        if param_ds_name is None:
            si_app.logger.warn('error: no data source name is given (ds_name)')
            result_message =   {'message_type': 'danger',
                                'message_title': 'Error',
                                'message_body':'No data source name is given (ds_name)'}


            base_navigation_dict = {'selected_menu': 'datasources',
                                    'dbrs': session.query(MDatasource),
                                    'error': 'error: no schema name is given',
                                    'selected_add_data_source': False,
                                    'message': result_message,
                                    'db': None
                                    }
            # self.rend
            # er("404.html")
            self.render("database_summary.html",  # current_schema_name = param_schema_name,
                        base_navigation_dict=base_navigation_dict )

        entry = None

        dbrs1 = session.query(MDatasource).filter_by(ds_name = param_ds_name )
        db = dbrs1.first()
        if db is None:
            print('')
            si_app.logger.warn('error: did not find database' + param_ds_name)
            result_message =   {'message_type': 'danger',
                                'message_title': 'Error',
                                'message_body':'error: did not find database' + param_ds_name}


            base_navigation_dict = {'selected_menu': 'overview',
                                    'dbrs': session.query(MDatasource),
                                    'error': 'error: no schema name is given',
                                    'selected_add_data_source': False,
                                    'message': result_message,
                                    'plugin_list': si_app.get_plugin_list(),
                                    }
            # self.render("404.html")
            self.render("overview.html",  # current_schema_name = param_schema_name,
                        base_navigation_dict=base_navigation_dict )

        dbrs = si_app.get_data_source_rs()
        tabrs = si_app.get_table_list_for_data_source_rs(param_ds_name= param_ds_name)

        base_navigation_dict = {'selected_menu': 'datasources',
                                'selected_add_data_source': False,
                                'dbrs': dbrs,
                                'selected_schema_name': param_ds_name,
                                'db':db,
                                'tabrs':tabrs,
                                'plugin_name_list': si_app.get_plugin_name_list(),
                                }


        base_navigation_dict['input_db_type'] = db.ds_type
        plugin_info = si_app.get_plugin_info(p_plugin_name=db.ds_type )
        base_navigation_dict['input_ds_param'] = json.loads(plugin_info.ds_param)

        self.render("database_summary.html", # current_schema_name = param_schema_name,
                    base_navigation_dict=base_navigation_dict # ,dbrs=dbrs, tabrs=tabrs,db=db
                    )

    def post(self):
        ds_dict = {}
        ds_dict['ds_name'] = self.get_argument('ds_name')
        ds_dict['ds_type'] = self.get_argument('ds_type')
        ds_dict['ds_desc'] = self.get_argument('ds_desc')

        ds_dict['ds_param'] = {}
        ds_plugin_info = si_app.get_plugin_info(p_plugin_name=ds_dict['ds_type'])
        param_name_dict = json.loads(ds_plugin_info.ds_param)
        for param_name in param_name_dict.keys():
            if param_name_dict[param_name]['type'] == 'Boolean':
                ds_dict['ds_param'][param_name] = self.get_argument('ds_param.' + param_name, default='off' )
            else:
                ds_dict['ds_param'][param_name] = self.get_argument('ds_param.' + param_name)

        db = si_app.update_data_soruce(ds_dict)


        dbrs = si_app.get_data_source_rs()

        result_message = {'message_type': 'info',
                          'message_title': 'Success',
                          'message_body': 'The data source %s is updated.' % (
                          str(ds_dict['ds_name']) )}

        base_navigation_dict = {'selected_menu': 'database',
                                'dbrs': dbrs,
                                'selected_add_data_source':False,
                                'selected_schema_name':ds_dict['ds_name'],
                                'plugin_name_list': si_app.get_plugin_name_list(),
                                'message': result_message,
                                'db':db  # When 'db' is available, it is treated as show_data_source
                                }


        base_navigation_dict['input_db_type'] = db.ds_type
        plugin_info = si_app.get_plugin_info(p_plugin_name=db.ds_type )
        base_navigation_dict['input_ds_param'] = json.loads(plugin_info.ds_param)

        self.render("database_summary.html",
                    base_navigation_dict=base_navigation_dict, dbrs=dbrs, db = None,tabrs=None)


class AddDataSourceHandler(tornado.web.RequestHandler):
    def get(self):
        #
        # it is import not to put 'db' into this dict to indicate this is add_data_source
        base_navigation_dict = {'selected_menu': 'datasources',
                                'dbrs': si_app.get_data_source_rs(),
                                'plugin_name_list': si_app.get_plugin_name_list(),
                                'selected_add_data_source':True,
                                'input_ds_param':True,
                                'selected_schema_name':'__add_data_source__',
                                }
        ds_type = self.get_argument('ds_type',default=None)


        if ds_type is None:
            ds_type =si_app.get_plugin_name_list()[0]  # simply choose first available plugin


        base_navigation_dict['input_db_type'] = ds_type
        plugin_info = si_app.get_plugin_info(p_plugin_name=ds_type)
        base_navigation_dict['input_ds_param'] = json.loads(plugin_info.ds_param)

        self.render("database_summary.html",
                    base_navigation_dict=base_navigation_dict,
                      db=None,tabrs=None)


    def post(self):
        ds_dict = {}
        ds_dict['ds_name'] = self.get_argument('ds_name')
        ds_dict['ds_desc'] = self.get_argument('ds_desc')
        ds_dict['ds_type'] = self.get_argument('ds_type')

        ds_dict['reflect_database_automatic'] = self.get_argument('reflect_database_automatic', default='off')

        ds_dict['ds_param'] = {}
        ds_plugin_info = si_app.get_plugin_info(p_plugin_name=ds_dict['ds_type'])
        param_name_dict = json.loads(ds_plugin_info.ds_param)
        for param_name in param_name_dict.keys():
            if param_name_dict[param_name]['type'] == 'Boolean':
                ds_dict['ds_param'][param_name] = self.get_argument('ds_param.' + param_name, default=False )
            else:
                ds_dict['ds_param'][param_name] = self.get_argument('ds_param.' + param_name)

        try:
            si_app.add_data_soruce(ds_dict)
            if(ds_dict['reflect_database_automatic'] =='on'):
                si_pm.reflect_db(ds_dict['ds_name'])

            #Info = {'result': 'ok', 'message': 'A new data source is added.'}
            self.redirect('/database_summary?ds_name=' + ds_dict['ds_name'])
        except Exception as e:
            si_app.logger.error('failed to add data source!')
            si_app.logger.error(e)
            #Info = {'result': 'ok', 'message': 'A new data source is added.'}
            dbrs = si_app.get_data_source_rs()
            result_message =   {'message_type': 'danger',
                                'message_title': 'Error',
                                'message_body':'Failed to add data source: %s! The error was: %s' % (str(ds_dict['ds_name']), str(e))}

            base_navigation_dict = {'selected_menu': 'database',
                                    'dbrs': dbrs,
                                    'selected_add_data_source': True,
                                    'plugin_name_list': si_app.get_plugin_name_list(),
                                    'selected_schema_name': ds_dict['ds_name'],
                                    'message': result_message,
                                    'db': MDatasource.from_dict(ds_dict = ds_dict),
                                    }
            base_navigation_dict['input_db_type'] = ds_dict['ds_type']
            plugin_info = si_app.get_plugin_info(p_plugin_name=ds_dict['ds_type'])
            base_navigation_dict['input_ds_param'] = json.loads(plugin_info.ds_param)


            self.render("database_summary.html",
                        base_navigation_dict=base_navigation_dict)

        '''
        dbrs = si_app.get_data_source_rs()

        Info = {'result': 'ok', 'message':'A new data source is added.'}
        base_navigation_dict = {'selected_menu': 'database',
                                'dbrs': dbrs,
                                'plugin_name_list': si_app.get_plugin_name_list(),
                                'selected_schema_name':ds_dict['ds_name'],
                                'db':db,
                                }
        self.render("database_summary.html",
                    base_navigation_dict=base_navigation_dict)
        '''

class DeleteDataSourceHandler(tornado.web.RequestHandler):
    def post(self):
        ds_name = self.get_argument('ds_name')
        ds_dict  = si_app.get_data_source_dict(ds_name=ds_name)
        ds_dict['delete_reflected_database_automatic'] = self.get_argument('delete_reflected_database_automatic', default=None)

        result_message = si_app.delete_data_soruce(ds_dict)
        dbrs = si_app.get_data_source_rs()
        base_navigation_dict = {'selected_menu': 'database',
                                'dbrs': dbrs,
                                'selected_add_data_source':True,
                                'plugin_name_list': si_app.get_plugin_name_list(),
                                'selected_schema_name':ds_dict['ds_name'],
                                'message': result_message
                                }
        if result_message['message_title']  == 'Error':
            session = create_session(bind=engine)
            dbrs1 = session.query(MDatasource).filter_by(ds_name = ds_dict['ds_name'])
            db = dbrs1.first()
            base_navigation_dict['db'] = db
            base_navigation_dict['tabrs'] = si_app.get_table_list_for_data_source_rs(param_ds_name= ds_dict['ds_name'])
            base_navigation_dict['input_db_type'] = ds_dict['ds_type']
            plugin_info = si_app.get_plugin_info(p_plugin_name=ds_dict['ds_type'])
            base_navigation_dict['input_ds_param'] = json.loads(plugin_info.ds_param)

            self.render("database_summary.html",
                        base_navigation_dict=base_navigation_dict)

        self.redirect('/')




class ReflectDataSourceHandler(tornado.web.RequestHandler):

    def post(self):
        ds_name = self.get_argument('ds_name')
        si_pm.reflect_db(ds_name)
        # self.__setattr__('reflected_db', ds_name)
        self.redirect('/database_summary?ds_name='+ds_name)


class ViewTableInNotebookHandler(tornado.web.RequestHandler):
    def get(self):
        # json.dumps()
        table_id = self.get_argument('table_id')
        ds_name = self.get_argument('ds_name')


        gen_loc = si_pm.generate_notebook_for_table(table_id=table_id, ds_name=ds_name)
        print(gen_loc)
        from subprocess import Popen
        p = Popen(["jupyter", "notebook",  "--notebook-dir=" + si_app.config['main']['schemaflex_spec'], gen_loc]) # something long running

        Info = {'result': 'started in another browser'}
        self.write(json.dumps(Info))








class DatabaseJSONHandler(tornado.web.RequestHandler):
    def post(self):
        ds_dict = {}
        # ds_dict['table_group_name']  = self.get_argument('table_group_name')
        ds_dict['ds_name'] = self.get_argument('ds_name')
        ds_dict['ds_url'] = self.get_argument('ds_url')
        ds_dict['ds_type'] = self.get_argument('ds_type')

        si_app.add_data_soruce(ds_dict)


        Info = {'result': 'ok'}
        self.write(json.dumps(Info))

    def get(self):
        # json.dumps()
        print('si_app.datasource_init()')
        si_app.datasource_init()
        db_dict = {'ds_name':'emp1'}
        self.write(json.dumps(db_dict)) # data = json.dumps(db_dict)

class SearchSuggestionJSONHandler(tornado.web.RequestHandler):
    def get(self):
        q = self.get_argument('query')
        res = si_app.get_whoosh_search_suggestion(q)
        self.write(json.dumps(res))
class SearchSuggestionWithFreqJSONHandler(tornado.web.RequestHandler):
    def get(self):
        q = self.get_argument('query')
        res = si_app.get_whoosh_search_suggestion_term_freq(q)
        self.write(json.dumps(res))
'''
class JSON1Handler(tornado.web.RequestHandler):
    def get(self):
        q = self.get_argument('query')
        res = si_app.get_whoosh_search_suggestion(q)
        self.write(json.dumps(res))

        # self.write(json.dumps(res1))
'''

class hdfs_inotify_get_checkpoint_txid(tornado.web.RequestHandler):
    def get(self):
        # Return Code:
        # -2 : Stop the process and wait for next notice
        # -1 : Start from last trx, as in hadoop inotification definition
        # Integer > 0 : the real trx id and proceed.

        #self.write('890')
        #return
        data_source_name = self.get_argument('data_source_name')
        ds_dict = si_app.get_data_source_dict(ds_name=data_source_name)
        if ds_dict['ds_param']['start_inotify'] == 'on' and ds_dict['last_reflect_date'] is not None:
            print('returning:' + str(ds_dict['ds_param']['inotify_trx_id']))
            self.write(str(ds_dict['ds_param']['inotify_trx_id']))
        else: # self.write('-1')
            self.write('-2')

class hdfs_inotify_change(tornado.web.RequestHandler):
    def post(self):
        event_type = self.get_argument('event_type')
        txid = self.get_argument('txid')
        data_source_name = self.get_argument('data_source_name')


        if event_type  == 'CREATE':
            path = self.get_argument('path')
            owner = self.get_argument('owner')
            date_time = self.get_argument('date_time')

            # /data/songs.csv._COPYING_
            if path[-9:] == '_COPYING_':
                # this is a intermidiate file, ignord.
                si_app.logger.info('this file is ignored because ._COPYING_ : ' + path)
                return

            print('event_type', event_type, "time", date_time,'tx:', txid, 'path:', path)

            doc_old = si_app.global_whoosh_search_by_id(q_id=path)
            if len(doc_old) > 0:
                si_app.logger.error('the doc/entity already not exist for creation event.')
                for doc1 in doc_old:
                    si_app.delete_doc_from_index_by_docnum(p_docnum=doc1['docnum'])

            si_app.add_table_content_index(ds_name = data_source_name,
                                           table_id=path,
                                           table_info=json.dumps({'path':path, 'date_time':date_time}),
                                           )


        # Do the thing
        elif event_type == 'UNLINK':
            path = self.get_argument('path')
            date_time = self.get_argument('date_time')

            doc_old = si_app.global_whoosh_search_by_id(q_id=path)
            if len(doc_old) < 1:
                si_app.logger.error('the doc/entity to delete/unlink does not exist.')
            else:
                si_app.delete_doc_from_index_by_docnum(p_docnum=doc_old[0]['docnum'])

            # si_app.commit_index()

            print('event_type', event_type, "time", date_time, 'tx:', txid)
        if event_type in 'RENAME':
            src_path = self.get_argument('src_path')
            dst_path = self.get_argument('dst_path')
            date_time = self.get_argument('date_time')

            doc_old = si_app.global_whoosh_search_by_id(q_id=src_path)
            if len(doc_old) < 1:
                si_app.logger.error('the doc/entity to rename does not exist.' + src_path)
            else:
                si_app.delete_doc_from_index_by_docnum(p_docnum=doc_old[0]['docnum'])

            doc_new = si_app.global_whoosh_search_by_id(q_id=dst_path)
            if len(doc_new) > 0:
                si_app.logger.error('the doc/entity already not exist for creation event.')
                for doc1 in doc_new:
                    si_app.delete_doc_from_index_by_docnum(p_docnum=doc1['docnum'])


            si_app.add_table_content_index(ds_name = data_source_name,
                                           table_id=dst_path,
                                           table_info=json.dumps({'path':dst_path, 'date_time':date_time}),
                                           )
            # si_app.commit_index()
            path = src_path + '.....' + dst_path
            print('event_type', event_type,'path',path, "time", date_time,'tx:', txid)
        else:
            print('event_type', event_type )

        print(path)

        # si_app.data_source_dict[data_source_name]['ds_param']['inotify_trx_id'] = txid


        #there may be performance issues if we update trxid everytime to database. Therefore, i updated to cache
        # most of times.

        # si_app.update_data_soruce(ds_dict=si_app.data_source_dict[data_source_name])
        si_app.update_data_soruce_trx_id(ds_name=data_source_name, trx_id=txid)

        self.write('received!' + path)







