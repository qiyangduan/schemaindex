plugin_name = 'mysql-native'

plugin_desc = 'mysql ReflectEngine'
supported_ds_types = ['mysql-native']

sample_ds_url = 'mysql://root:xyz@localhost/employees'
author = 'duan'

class_name = 'mysqlflex.MysqlReflectEngine'

from .mysqlreflectengine import MysqlReflectEngine as ReflectEngine
