plugin_name = 'sqlite'

plugin_desc = 'mysql ReflectEngine'
supported_ds_types = ['sqlite3']

sample_ds_url = 'lite://root:xyz@localhost/employees'
author = 'duan'

class_name = 'a.b'

from .sqliteengine import SQLAlchemyReflectEngine as ReflectEngine
