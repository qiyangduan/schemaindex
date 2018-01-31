#!/usr/bin/env python

import os.path

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.web

from . import config
from . import handler

# from app import dbmodels

class MApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", handler.OverviewHandler),
            (r"/overview", handler.OverviewHandler),
            (r"/database_json", handler.DatabaseJSONHandler),
            (r"/database_summary", handler.DatabaseSummaryHandler),
            (r"/add_data_source", handler.AddDataSourceHandler),
            (r"/delete_data_source", handler.DeleteDataSourceHandler),
            (r"/relfect_data_source", handler.ReflectDataSourceHandler),
            (r"/view_table_in_notebook", handler.ViewTableInNotebookHandler),
            #

            (r"/reload_plugins", handler.ReloadPluginHandler),
            (r"/global_search", handler.GlobalSearchHandler),
            (r"/search_suggestion_json", handler.SearchSuggestionJSONHandler),
            (r"/search_suggestion_freq", handler.SearchSuggestionWithFreqJSONHandler),

            (r"/hdfs_inotify_change", handler.hdfs_inotify_change),
            (r"/hdfs_inotify_get_checkpoint_txid", handler.hdfs_inotify_get_checkpoint_txid),

        ]
        settings = dict(
            website_title=u"Schema Index",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            # ui_modules={"Entry": EntryModule},
            xsrf_cookies=False,
            cookie_secret="databasemodels:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True,
        )
        super(MApplication, self).__init__(handlers, **settings)
        # Have one global connection to the blog DB across all handlers
        # self.engine = engine

def run_webserver(addr = None, port=8088):
    tornado.options.parse_command_line()
    app = tornado.httpserver.HTTPServer(MApplication())
    if addr is None:
        app.listen(port=port)
    else:
        app.listen(port=port, address=addr)

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run_webserver(port = config.cfg['web']['port'], addr = config.cfg['web']['address'])


'''    tornado.options.parse_command_line()
    app = tornado.httpserver.HTTPServer(MApplication())
    app.listen(config.cfg['web']['port'])
    tornado.ioloop.IOLoop.current().start()
'''