plugin_name = 'sqlalchemy'
plugin_desc = 'Sqlalchemy reflect engine, which works for many mainstream databases, including Mysql, Sqlite, etc. For mysql to work, you need to install pymysql/mysqlclient (python3) or mysql-python (python2) in advance.'
supported_ds_types = ['mysql','sqlite3']


ds_param = {'schema_name': {'type':'String',
                             'full_name':'Schema Name to Reflect:',
                             'desc':'''''',
                             },
            'connect_string': {'type':'String',
                             'full_name':'Database Connection String:',
                             'desc':'''The sqlalchemy access URL,  for example: mysql://root:xyz@localhost/employees.''',
                             },
            }


sample_ds_url = 'mysql://root:xyz@localhost/employees'

author = 'duan'
class_name = 'sqlalchemyindex.SQLAlchemyReflectEngine'
notebook_template_path = 'show_sqlalchemy_table_template.ipynb'

from .sqlalchemyengine import SQLAlchemyReflectEngine as ReflectEngine
