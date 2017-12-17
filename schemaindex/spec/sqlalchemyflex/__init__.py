plugin_name = 'sqlalchemy'
plugin_desc = 'mysql ReflectEngine'
supported_ds_types = ['mysql','sqlite3']


ds_param = {'schema_name': {'type':'String',
                             'full_name':'Schema Name to Reflect:',
                             'desc':'''''',
                             },
            'ds_url': {'type':'String',
                             'full_name':'Database Connection String:',
                             'desc':'''The sqlalchemy access URL,  for example: mysql://root:xyz@localhost/employees.''',
                             },
            }


sample_ds_url = 'mysql://root:xyz@localhost/employees'

author = 'duan'
class_name = 'sqlalchemyflex.SQLAlchemyReflectEngine'
notebook_template_path = 'show_sqlalchemy_table_template.ipynb'

from .sqlalchemyengine import SQLAlchemyReflectEngine as ReflectEngine
