import os, sys
import traceback, logging

# Those are all options for end user to customize. Other internal configurations may be found in different classes.
cfg = {"web": {
                'port': 8088,
                'address': "localhost",
                'use_anonymous' : True
               },
        'database': {
                'ds_type': 'sqlite3',
                'sqlite_file':  os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__))), '..' , "schemaindex.sqlite3") ,
                'user': 'root',
                'passwd': 'my secret password',
                },
        "main": {"schemaflex_home": os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
                 "schemaflex_spec": os.path.abspath(os.path.join(os.path.dirname(__file__), '..','plugin')),
                 "schemaindex_notebooks": os.path.abspath(os.path.join(os.path.dirname(__file__), '..','notebooks')),
                 "schemaflex_text_index_path": os.path.abspath(os.path.join(os.path.dirname(__file__), '..','indexdir')),
                 'init_indicator_file': os.path.abspath(os.path.join(os.path.dirname(__file__), 'do_schemaindex_init')),
                 'interval_commit_trx_id': 60,
                 'search_result_limit': 100,
                 },
        "logging": {"log_file": "schemaindex.log",
                            "log_dir": "log",
                            "log_level": "DEBUG"  # DEBUG,INFO,WARNING,ERROR,CRITICAL
                            }
}

sys.path.append( cfg['main']['schemaflex_spec'])

if not os.path.exists(cfg['main']['schemaflex_spec']):
    os.mkdir(cfg['main']['schemaflex_spec'])


LOG_DIR = os.path.join(cfg['main']['schemaflex_home'],
                       cfg['logging']['log_dir'])
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)



current_logfile_path = os.path.join(LOG_DIR,
                                    cfg['logging']['log_file'])


class MyStreamHandler(logging.StreamHandler):
    def format(self, record):
        try:
            return logging.StreamHandler.format(self, record)
        except TypeError:
            # Print a stack trace that includes the original log call
            traceback.print_stack()

    def handleError(self, record):
        raise


logging.basicConfig(format='[%(asctime)s] {%(pathname)s:%(lineno)d}  - %(message)s',
                    level=logging.getLevelName(cfg['logging']['log_level']),
                    filename=current_logfile_path)

log = logging.getLogger('schemaflex_logger')
handler = MyStreamHandler()
log.addHandler(handler)

# logging.getLogger('schemaflex_logger').info('Logging initialization finished.')  # will not print anything


class SchemaIndexPluginError(Exception):
    pass


