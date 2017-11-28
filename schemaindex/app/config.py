import os
import traceback, logging

# Those are all options for end user to customize. Other internal configurations may be found in different classes.
cfg = {"web": {
                'port': 8088,
                'use_anonymous' : True
               },
        'database': {
                'db_type': 'sqlite3',
                'sqlite_file': "allmodel.sqlite3",
                'user': 'root',
                'passwd': 'my secret password',
                },
        "main": {"schemaflex_home": os.path.abspath(os.path.join(os.path.dirname(__file__), '..')),
                 "schemaflex_text_index_path": os.path.abspath(os.path.join(os.path.dirname(__file__), '..','indexdir')),
                 'init_indicator_file': os.path.abspath(os.path.join(os.path.dirname(__file__), 'do_schemaindex_init')),
                 },
        "logging": {"log_file": "schemaindex.log",
                            "sqla_log_file": "schemaflex_sqlalchemy.log",
                            "root_log_file": "schemaflex_others.log",
                            "log_dir": "log",
                            "log_level": "ERROR"  # DEBUG,INFO,WARNING,ERROR,CRITICAL
                            }
}


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
# logging.basicConfig()
logging.getLogger('sqlalchemyflex.engine').setLevel(logging.ERROR)
logging.getLogger('sqlalchemyflex').setLevel(logging.ERROR)
logging.getLogger('sqlalchemyflex.engine.base.Engine').setLevel(logging.ERROR)

sqla_logger = logging.getLogger('sqlalchemyflex')
sqla_logger.propagate = False
sqla_logger.addHandler(logging.FileHandler(os.path.join(LOG_DIR, cfg['logging']['sqla_log_file'])))
logging.getLogger('sqlalchemyflex.engine').addHandler(
    logging.FileHandler(os.path.join(LOG_DIR, cfg['logging']['sqla_log_file'])))
logging.getLogger().addHandler(
    logging.FileHandler(os.path.join(LOG_DIR, cfg['logging']['root_log_file'])))

# log.error("Now try passing a string to an int: %d", 'abc')
# log.error("Try interpolating an int correctly: %i", 1)
# log.error("Now try passing a string to an int: %d", 'abc')
# log.error("And then a string to a string %s", 'abc')
logging.getLogger('schemaflex_logger').info('Logging initialization finished.')  # will not print anything


class schemaflexError(Exception):
    pass


class schemaflexParameterError(Exception):
    pass


class schemaflexErrorNoInstanceID(Exception):
    pass
