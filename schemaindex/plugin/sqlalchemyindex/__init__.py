plugin_name = 'sqlalchemy'
plugin_desc = 'Sqlalchemy reflect engine, which works for many mainstream databases, including Mysql, Sqlite, etc. For each db to work, you need to install pymysql/mysqlclient (python3) or mysql-python (python2) in advance.'
supported_ds_types = ['mysql','sqlite3']
required_packages = []


ds_param = {'schema_name': {'type':'String',
                             'full_name':'Schema Name to Reflect:',
                             'default_value': '_NA',
                             'desc':'''''',
                             },
            'connect_string': {'type':'String',
                             'full_name':'Database Connection String:',
                             'default_value': 'sqlite:////tmp/db1',
                             'desc':'''The sqlalchemy access URL.''',
                             },
            }


sample_ds_url = 'mysql://root:xyz@localhost/employees'
metadata_type='table'

author = 'duan'
class_name = 'sqlalchemyindex.SQLAlchemyReflectEngine'
notebook_template_path = 'show_sqlalchemy_table_template.ipynb'

from .sqlalchemyengine import SQLAlchemyReflectEngine as ReflectEngine
