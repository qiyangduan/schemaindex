from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import web
import os
import json
# import tornado.web

from schemaindex.app.schemaindexapp import si_app  #
from schemaindex.app.pluginmanager import si_pm  #



SI_TEMPLATE_DIR = os.path.join(si_app.config['main']['schemaflex_home']
                               , 'app','templates'
                               )
# '/home/duan/github/schemaindex/schemaindex/app/templates'
SI_STATIC_DIR = os.path.join(si_app.config['main']['schemaflex_home']
                               , 'app','static'
                               )


def _jupyter_server_extension_paths():
    return [{
        "module": "schemaindex.jupyterext.serverext.schemaindex_serverext"
    }]


class SchemaindexGenerateSnippetHandler(IPythonHandler):
    def get(self):
        table_id = self.get_argument('table_id')
        ds_name = self.get_argument('ds_name')
        # print('i got parameter' + table_id + 'i got parameter' + ds_name)

        res = si_pm.generate_notebook_snippet_for_table(table_id=table_id,
                                                        ds_name=ds_name)
        # print('i got result:' + str(res))

        self.write(str(res))  #



class SchemaindexSearchFormattedHandler(IPythonHandler):
    def get(self):
        q = self.get_argument('q')
        # print('i got parameter' + q)
        if(q=='*'):
            ds = self.get_argument('ds_name')
            res = si_app.global_whoosh_search_by_ds(ds_name=ds)
        else:
            res = si_app.global_whoosh_search_formatted(q)

        # print('i got result:' + str(res))
        self.write(json.dumps(res))  # res) #

class SchemaindexStatisticsHandler(IPythonHandler):

    @web.authenticated
    def get(self):
        res = si_app.get_schemaindex_statistics()
        # print('i got result:' + str(res))
        # print(self.settings['jinja2_env'].loader.searchpath)
        self.write(json.dumps(res))  # res) #

class SchemaindexSearchSuggestionJSONHandler( IPythonHandler):
    def get(self):
        q = self.get_argument('query')
        res = si_app.get_whoosh_search_suggestion_term_freq(q)
        self.write(json.dumps(res))

class SchemaindexBaseURLHandler( IPythonHandler):
    def get(self):
        u = str(si_app.nb_web_app.settings)
        self.write( u)

class SchemaindexTest1Handler(IPythonHandler):
    def get(self):
        #print(self.settings['jinja2_env'].loader.searchpath)
        #self.settings['jinja2_env'].loader.searchpath.append('/home/duan/github/schemaindex/schemaindex/app/templates')
        #print(self.settings['jinja2_env'].loader.searchpath)

        self.write( self.render_template('duan.html',
                        mes='hello world again!!!!',
                        )
                   )


class OverviewHandler(IPythonHandler):
    @web.authenticated
    def get(self):
        # self.write("Hello, world")
        dbrs = si_app.get_data_source_rs()

        ds_count = dbrs.count()
        base_navigation_dict = {'selected_menu': 'overview',
                                'dbrs': dbrs,
                                'plugin_list': si_app.get_plugin_list(),
                                'ds_count':str(ds_count),
        }

        self.write(self.render_template('overview.html',
                                         base_navigation_dict=base_navigation_dict,
                                        )
                   )



class DatabaseSummaryHandler( IPythonHandler):
    @web.authenticated
    def get(self):
        # self.write("Hello, world")
        # param_db_name = self.get_argument("table_group_name", None)
        # session = create_session(bind=engine)
        print(self.request.path)
        param_ds_name = self.get_argument("ds_name", None)
        if param_ds_name is None:
            si_app.logger.warn('error: no data source name is given (ds_name)')
            result_message =   {'message_type': 'danger',
                                'message_title': 'Error',
                                'message_body':'No data source name is given (ds_name)'}


            base_navigation_dict = {'selected_menu': 'datasources',
                                    'dbrs': si_app.get_data_source_rs(), # session.query(MDatasource),
                                    'error': 'error: no schema name is given',
                                    'selected_add_data_source': False,
                                    'message': result_message,
                                    'db': None,
                                    'self.request.path':self.request.path,
                                    }
            # self.rend
            self.write(self.render_template('database_summary.html',
                                            base_navigation_dict=base_navigation_dict,
                                            )
                       )

        #dbrs1 = session.query(MDatasource).filter_by(ds_name = param_ds_name )
        # db = dbrs1.first()


        # 20180120, changed db from MDatasoruce to ds_dict.
        db = si_app.get_data_source_dict(ds_name=param_ds_name)
        if db is None:
            print('')
            si_app.logger.warn('error: did not find database' + param_ds_name + ' after creation.')
            result_message =   {'message_type': 'danger',
                                'message_title': 'Error',
                                'message_body':'error: did not find database' + param_ds_name}


            base_navigation_dict = {'selected_menu': 'overview',
                                    'dbrs': si_app.get_data_source_rs(), # session.query(MDatasource),
                                    'error': 'error: no schema name is given',
                                    'selected_add_data_source': False,
                                    'message': result_message,
                                    'self.request.path':self.request.path,
                                    'plugin_list': si_app.get_plugin_list(),
                                    }

            self.write(self.render_template('database_summary.html',
                                            base_navigation_dict=base_navigation_dict,
                                            )
                       )


        dbrs = si_app.get_data_source_rs()
        tabrs = si_app.get_table_list_for_data_source_rs(param_ds_name= param_ds_name)

        base_navigation_dict = {'selected_menu': 'datasources',
                                'selected_add_data_source': False,
                                'dbrs': dbrs,
                                'selected_schema_name': param_ds_name,
                                'db':db,
                                'tabrs':tabrs,
                                'self.request.path': self.request.path,
                                'plugin_name_list': si_app.get_plugin_name_list(),
                                }


        base_navigation_dict['input_db_type'] = db['ds_type']
        plugin_info = si_app.get_plugin_info(p_plugin_name=db['ds_type'] )
        base_navigation_dict['input_ds_param'] = json.loads(plugin_info.ds_param)

        self.write(self.render_template('database_summary.html',
                                        base_navigation_dict=base_navigation_dict,
                                        )
                   )

    @web.authenticated
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
                                'self.request.path': self.request.path,
                                'db':db.to_dict(),   # When 'db' is available, it is treated as show_data_source
                                }


        base_navigation_dict['input_db_type'] = db.ds_type
        plugin_info = si_app.get_plugin_info(p_plugin_name=db.ds_type )
        base_navigation_dict['input_ds_param'] = json.loads(plugin_info.ds_param)

        #self.render("database_summary.html",
        #            base_navigation_dict=base_navigation_dict, dbrs=dbrs, db = None,tabrs=None)
        self.write(self.render_template('database_summary.html',
                                        base_navigation_dict=base_navigation_dict,
                                        )
                   )

class AddDataSourceHandler( IPythonHandler):
    @web.authenticated
    def get(self):
        #
        # it is import not to put 'db' into this dict to indicate this is add_data_source
        base_navigation_dict = {'selected_menu': 'datasources',
                                'self.request.path': self.request.path,
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

        #self.render("database_summary.html",
        #            base_navigation_dict=base_navigation_dict,
        #              db=None,tabrs=None)
        self.write(self.render_template('database_summary.html',
                                        base_navigation_dict=base_navigation_dict,
                                        )
                   )

    @web.authenticated
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
            self.redirect('./database_summary?ds_name=' + ds_dict['ds_name'])
        except Exception as e:
            si_app.logger.error('failed to add data source!')
            si_app.logger.error(e)
            #Info = {'result': 'ok', 'message': 'A new data source is added.'}
            dbrs = si_app.get_data_source_rs()
            result_message =   {'message_type': 'danger',
                                'message_title': 'Error',
                                'message_body':'Failed to add data source: %s! The error was: %s' % (str(ds_dict['ds_name']), str(e))}

            base_navigation_dict = {'selected_menu': 'database',
                                    'self.request.path': self.request.path,
                                    'dbrs': dbrs,
                                    'selected_add_data_source': True,
                                    'plugin_name_list': si_app.get_plugin_name_list(),
                                    'selected_schema_name': ds_dict['ds_name'],
                                    'message': result_message,
                                    'db':  ds_dict,
                                    }
            base_navigation_dict['input_db_type'] = ds_dict['ds_type']
            plugin_info = si_app.get_plugin_info(p_plugin_name=ds_dict['ds_type'])
            base_navigation_dict['input_ds_param'] = json.loads(plugin_info.ds_param)


            #self.render("database_summary.html",
            #            base_navigation_dict=base_navigation_dict)
            self.write(self.render_template('database_summary.html',
                                            base_navigation_dict=base_navigation_dict,
                                            )
                       )


class DeleteDataSourceHandler( IPythonHandler):
    @web.authenticated
    def post(self):
        ds_name = self.get_argument('ds_name')
        ds_dict  = si_app.get_data_source_dict(ds_name=ds_name)
        ds_dict['delete_reflected_database_automatic'] = self.get_argument('delete_reflected_database_automatic', default=None)

        result_message = si_app.delete_data_soruce(ds_dict)
        dbrs = si_app.get_data_source_rs()
        base_navigation_dict = {'selected_menu': 'database',
                                'self.request.path': self.request.path,
                                'dbrs': dbrs,
                                'selected_add_data_source':True,
                                'plugin_name_list': si_app.get_plugin_name_list(),
                                'selected_schema_name':ds_dict['ds_name'],
                                'message': result_message
                                }
        if result_message['message_title']  == 'Error':
            #session = create_session(bind=engine)
            #dbrs1 = session.query(MDatasource).filter_by(ds_name = ds_dict['ds_name'])
            #db = dbrs1.first()
            base_navigation_dict['db'] = ds_dict
            base_navigation_dict['tabrs'] = si_app.get_table_list_for_data_source_rs(param_ds_name= ds_dict['ds_name'])
            base_navigation_dict['input_db_type'] = ds_dict['ds_type']
            plugin_info = si_app.get_plugin_info(p_plugin_name=ds_dict['ds_type'])
            base_navigation_dict['input_ds_param'] = json.loads(plugin_info.ds_param)

            #self.render("database_summary.html",
            #            base_navigation_dict=base_navigation_dict)

            self.write(self.render_template('database_summary.html',
                                            base_navigation_dict=base_navigation_dict,
                                            )
                       )

        self.redirect('./overview')




class ReflectDataSourceHandler( IPythonHandler):

    @web.authenticated
    def post(self):
        ds_name = self.get_argument('ds_name')
        si_pm.reflect_db(ds_name)
        # self.__setattr__('reflected_db', ds_name)
        self.redirect('./database_summary?ds_name='+ds_name)


class ViewTableInNotebookHandler( IPythonHandler):
    @web.authenticated
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


class ReloadPluginHandler(IPythonHandler):
    @web.authenticated
    def get(self):
        si_pm.scan_reflect_plugins()
        '''
        dbrs = si_app.get_data_source_rs()
        ds_count = dbrs.count()

        base_navigation_dict = {'selected_menu': 'overview',
                                'dbrs': dbrs,
                                'plugin_list': si_app.get_plugin_list(),
                                'ds_count':str(ds_count),
        }
        '''
        # self.render("overview.html", base_navigation_dict=base_navigation_dict)
        self.redirect('./overview')



class GenerateNotebookHandler(IPythonHandler):
    @web.authenticated
    def get(self):
        table_id = self.get_argument('table_id')
        ds_name = self.get_argument('ds_name')



        ds_dict = si_app.get_data_source_dict(ds_name= ds_name)
        the_engine = si_pm.get_reflect_plugin(ds_dict['ds_type'])['reflect_engine']
        a_ds = the_engine.ReflectEngine(ds_dict = ds_dict )
        new_snippet = a_ds.generate_notebook_snippet(table_id= table_id)

        replace_dict = {'$$cell1$$': '\\n'.join(new_snippet.split('\n')),
                        '$$cell2$$': ''}

        # print(si_app.nb_server_app.__dict__)
        print('the config is: ', si_app.nb_server_app.config.__dict__)
        n_root_dir1 = si_app.nb_server_app.config['FileContentsManager']['root_dir']
        n_root_dir = si_app.nb_server_app.notebook_dir
        print(n_root_dir)
        notebook_file_name = '__'.join(('si_notebook_' + ds_name + '_' + table_id + '.ipynb').split('/'))
        generate_path = os.path.join(str(n_root_dir), notebook_file_name)
        print(generate_path)
        with open(os.path.join(si_app.config['main']['schemaflex_home'],'jupyterext', 'schemaindex_notebook_template.ipynb'), "rt") as fin:
            with open( generate_path, "wt") as fout:
                for line in fin:
                    snippet_result = line
                    for key in replace_dict.keys():
                        snippet_result = snippet_result.replace(key, replace_dict[key])
                    fout.write(snippet_result)

        #from subprocess import Popen
        #p = Popen(["jupyter", "notebook",  "--notebook-dir=" + si_app.config['main']['schemaflex_spec'], gen_loc]) # something long running

        # Info = {'result': 'started in another browser'}
        self.redirect(url=url_path_join(si_app.nb_server_app.web_app.settings['base_url'], 'notebooks', notebook_file_name))


class GlobalSearchHandler( IPythonHandler):
    @web.authenticated
    def get(self):
        q = ''
        res = []
        dbrs = si_app.get_data_source_rs()

        base_navigation_dict = {'selected_menu': 'search',
                                'dbrs': dbrs,
                                'selected_schema_name': '',
                                'q':q,
                                'search_result':res,
                                }
        '''
        self.render("global_search_result.html",
                    dbrs=dbrs,
                    q=q,
                    base_navigation_dict=base_navigation_dict,
                    search_result = res )
        '''
        self.write(self.render_template('global_search_result.html',
                                        base_navigation_dict=base_navigation_dict,
                                        )
                   )

    @web.authenticated
    def post(self):

        q = self.get_argument('q')
        res = si_app.global_whoosh_search(q)
        dbrs = si_app.get_data_source_rs()

        base_navigation_dict = {'selected_menu': 'search',
                                'dbrs': dbrs,
                                'selected_schema_name': '',
                                'q':q,
                                'search_result':res,
                                }
        self.write(self.render_template('global_search_result.html',
                                        base_navigation_dict=base_navigation_dict,
                                        )
                   )


class SearchSuggestionJSONHandler(IPythonHandler):
    @web.authenticated
    def get(self):
        q = self.get_argument('query')
        res = si_app.get_whoosh_search_suggestion(q)
        self.write(json.dumps(res))

class SearchSuggestionWithFreqJSONHandler(IPythonHandler):
    @web.authenticated
    def get(self):
        q = self.get_argument('query')
        res = si_app.get_whoosh_search_suggestion_term_freq(q)
        self.write(json.dumps(res))

class DatabaseJSONHandler(IPythonHandler):
    @web.authenticated
    def post(self):
        ds_dict = {}
        # ds_dict['table_group_name']  = self.get_argument('table_group_name')
        ds_dict['ds_name'] = self.get_argument('ds_name')
        ds_dict['ds_url'] = self.get_argument('ds_url')
        ds_dict['ds_type'] = self.get_argument('ds_type')

        si_app.add_data_soruce(ds_dict)

        Info = {'result': 'ok'}
        self.write(json.dumps(Info))

    @web.authenticated
    def get(self):
        # json.dumps()
        print('si_app.datasource_init()')
        si_app.datasource_init()
        db_dict = {'ds_name': 'emp1'}
        self.write(json.dumps(db_dict))  # data = json.dumps(db_dict)


# ######################################################################
# ----------------------------------------------------------------------


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """

    nb_server_app.log.info("schemaindex server extension is loaded!")
    web_app = nb_server_app.web_app
    si_app.nb_server_app = nb_server_app

    # print(nb_server_app.__dict__)
    # print("default path:" + nb_server_app.notebook_dir) # root_dir
    # si_app.notebook_dir = nb_server_app.notebook_dir

    #print("static path:" + nb_server_app.extra_static_paths)
    #print(web_app.settings['jinja2_env'])
    #print(web_app.settings['jinja2_env'].loader.searchpath)
    # https://github.com/pallets/jinja/blob/bbe0a4174c2846487bef4328b309fddd8638da39/jinja2/loaders.py
    if SI_TEMPLATE_DIR not in web_app.settings['jinja2_env'].loader.searchpath:
        web_app.settings['jinja2_env'].loader.searchpath.append(SI_TEMPLATE_DIR)
        print('Added schemaindex template file location: ', SI_TEMPLATE_DIR)

    # print(self.settings['jinja2_env'].loader.searchpath)
    # self.settings['jinja2_env'].loader.searchpath.append('/home/duan/github/schemaindex/schemaindex/app/templates')
    # print(self.settings['jinja2_env'].loader.searchpath)


    # nb_server_app.extra_template_paths.append(template_path)
    #print("template path:" + nb_server_app.extra_template_paths)

    # nb_server_app.extra_static_paths = ['/home/duan/github/schemaindex/schemaindex/app/static']

    si_app.nb_web_app =  web_app # .settings['base_url']
    host_pattern = '.*$'

    route_handler = [# (url_path_join(web_app.settings['base_url'], '/schemaindex', '/global_search'),  SchemaindexSearchHandler),
                     (url_path_join(web_app.settings['base_url'], '/schemaindex', '/global_search_formatted'),
                      SchemaindexSearchFormattedHandler),
                     (url_path_join(web_app.settings['base_url'], '/schemaindex', '/search_suggestion_json'),
                      SchemaindexSearchSuggestionJSONHandler),
                     (url_path_join(web_app.settings['base_url'], '/schemaindex', '/generate_snippet'),
                      SchemaindexGenerateSnippetHandler),
                     (url_path_join(web_app.settings['base_url'], '/schemaindex', '/get_schemaindex_base_rul'),
                      SchemaindexBaseURLHandler),
                     (url_path_join(web_app.settings['base_url'], '/schemaindex', '/get_schemaindex_statistics'),
                      SchemaindexStatisticsHandler),
                     (url_path_join(web_app.settings['base_url'], '/schemaindex', '/test1'),
                      SchemaindexTest1Handler),

                     ]
    web_app.add_handlers(host_pattern, route_handler)
    # print(nb_server_app.template_path)

    web_app.add_handlers('.*$',  [( url_path_join(web_app.settings['base_url'],  'static/schemaindex_static/(.*)'),
                                   web.StaticFileHandler, {'path': SI_STATIC_DIR})]),
    url_pref = url_path_join(web_app.settings['base_url'], '/schemaindex')

    si_route_handler = [(url_path_join(url_pref, '/overview'),    OverviewHandler),
                        (url_path_join(url_pref, '/database_summary'), DatabaseSummaryHandler),
                        (url_path_join(url_pref, '/add_data_source'), AddDataSourceHandler),
                        (url_path_join(url_pref, '/delete_data_source'), DeleteDataSourceHandler),
                        (url_path_join(url_pref, '/relfect_data_source'), ReflectDataSourceHandler),
                        (url_path_join(url_pref, '/view_table_in_notebook'), ViewTableInNotebookHandler),
                        #reload_plugins
                        (url_path_join(url_pref, '/reload_plugins'), ReloadPluginHandler),
                        #
                        (url_path_join(url_pref, '/global_search'), GlobalSearchHandler),
                        (url_path_join(url_pref, '/search_suggestion_json_orig'), SearchSuggestionJSONHandler),
                        (url_path_join(url_pref, '/search_suggestion_freq'), SearchSuggestionWithFreqJSONHandler),
                        (url_path_join(url_pref, '/database_json'), DatabaseJSONHandler),
                        (url_path_join(url_pref, '/generate_notebook'), GenerateNotebookHandler),
                        ]

    web_app.add_handlers(host_pattern, si_route_handler)




################################
# Not useful
################################
class SchemaindexSearchHandler(IPythonHandler):
    def get(self):
        q = self.get_argument('q')
        # print('i got parameter' + q)

        res = si_app.global_whoosh_search(q)
        # print('i got result:' + str(res))

        self.write(json.dumps(res))  # res) #
