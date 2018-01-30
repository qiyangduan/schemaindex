from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler

import json
import tornado.web

from schemaindex.app.schemaindexapp import si_app  #
from schemaindex.app.pluginmanager import si_pm  #


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


class SchemaindexSearchHandler(IPythonHandler):
    def get(self):
        q = self.get_argument('q')
        # print('i got parameter' + q)

        res = si_app.global_whoosh_search(q)
        # print('i got result:' + str(res))

        self.write(json.dumps(res))  # res) #

class SchemaindexSearchFormattedHandler(IPythonHandler):
    def get(self):
        q = self.get_argument('q')
        # print('i got parameter' + q)

        res = si_app.global_whoosh_search_formatted(q)
        # print('i got result:' + str(res))

        self.write(json.dumps(res))  # res) #

class SchemaindexStatisticsHandler(IPythonHandler):
    def get(self):
        res = si_app.get_schemaindex_statistics()
        # print('i got result:' + str(res))
        self.write(json.dumps(res))  # res) #



class SchemaindexSearchSuggestionJSONHandler(tornado.web.RequestHandler):
    def get(self):
        q = self.get_argument('query')
        res = si_app.get_whoosh_search_suggestion_term_freq(q)
        self.write(json.dumps(res))

class SchemaindexBaseURLHandler(tornado.web.RequestHandler):
    def get(self):
        u = str(si_app.nb_web_app.settings)
        self.write( u)

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    nb_server_app.log.info("schemaindex server extension is loaded!")
    web_app = nb_server_app.web_app

    si_app.nb_web_app =  web_app # .settings['base_url']
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/schemaindex', '/global_search')
    route_handler = [(route_pattern, SchemaindexSearchHandler),
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
                     ]
    web_app.add_handlers(host_pattern, route_handler)




class GlobalSearchHandler(IPythonHandler):
    def get(self):
        q = self.get_argument('q')
        res = ''
        if q == '1':
            res = '[{"column_info": [["ds_name", "VARCHAR(100)", null], ["table_group_name", "VARCHAR(200)", null], ["table_name", "VARCHAR(255)", null], ["table_type", "VARCHAR(255)", null], ["table_comment", "VARCHAR(5000)", null]], "table_group_name": "na", "table_name": "mtable", "ds_name": "q"}]'
        elif q == '2':
            res = ''' [ {"column_info": [["ds_name", "VARCHAR(100)", null], ["table_group_name", "VARCHAR(200)", null], ["table_name", "VARCHAR(255)", null], ["table_type", "VARCHAR(255)", null], ["table_comment", "VARCHAR(5000)", null]], "table_group_name": "na", "table_name": "mtable", "ds_name": "q"}
                  , 	{"column_info": [["ds_name", "VARCHAR(100)", null], ["nbr_of_tables", "INTEGER", null], ["nbr_of_columns", "INTEGER", null], ["ds_type", "VARCHAR(100)", null], ["created_date", "DATETIME", null], ["last_reflect_date", "DATETIME", null], ["ds_param", "VARCHAR(4000)", null], ["ds_desc", "VARCHAR(1000)", null], ["ds_tags", "VARCHAR(2550)", null]], "table_group_name": "na", "table_name": "mdatasource", "ds_name": "q"}
                  ]
                  '''
        else:
            res = '[]'
        self.write(res)  # json.dumps(res))

    def post(self):
        q = self.get_argument('q')
        print('i got parameter' + q)
        res = ''
        if q == '1':
            res = '[{"column_info": [["ds_name", "VARCHAR(100)", null], ["table_group_name", "VARCHAR(200)", null], ["table_name", "VARCHAR(255)", null], ["table_type", "VARCHAR(255)", null], ["table_comment", "VARCHAR(5000)", null]], "table_group_name": "na", "table_name": "mtable", "ds_name": "q"}]'
        elif q == '2':
            res = ''' [ {"column_info": [["ds_name", "VARCHAR(100)", null], ["table_group_name", "VARCHAR(200)", null], ["table_name", "VARCHAR(255)", null], ["table_type", "VARCHAR(255)", null], ["table_comment", "VARCHAR(5000)", null]], "table_group_name": "na", "table_name": "mtable", "ds_name": "q"}
                  , 	{"column_info": [["ds_name", "VARCHAR(100)", null], ["nbr_of_tables", "INTEGER", null], ["nbr_of_columns", "INTEGER", null], ["ds_type", "VARCHAR(100)", null], ["created_date", "DATETIME", null], ["last_reflect_date", "DATETIME", null], ["ds_param", "VARCHAR(4000)", null], ["ds_desc", "VARCHAR(1000)", null], ["ds_tags", "VARCHAR(2550)", null]], "table_group_name": "na", "table_name": "mdatasource", "ds_name": "q"}
                  ]
                  '''
        else:
            res = '[]'
        self.write(res)  # json.dumps(res))

class SearchSuggestionJSONHandler(tornado.web.RequestHandler):
    def get(self):
        q = self.get_argument('query')
        res = {}
        if q == 'ta':
            res = [{"ds_name": "1", "table_id": "table"},
                   {"ds_name": "2", "table_id": "tags"},
                   ]

        elif q == 'mta':
            res = [{"data": [{"ds_name": "3", "display": "mtable"},
                             ]
                    }]
        else:
            res = [{"ds_name": "5", "table_id": "table"},
                   {"ds_name": "6", "table_id": "tags"},
                   ]

        self.write(json.dumps(res))

    def post(self):
        q = self.get_argument('query')
        res = {}
        if q == 'ta':
            res = {"data": [{"ds_name": "1", "display": "table"},
                            {"ds_name": "2", "display": "tags"},
                            ]
                   }
        elif q == 'mta':
            res = {"data": [{"ds_name": "3", "display": "mtable"},
                            ]
                   }
        else:
            res = {"data": [{"ds_name": "5", "display": "table"},
                            {"ds_name": "6", "display": "tags"},
                            ]
                   }

        self.write(json.dumps(res))
