plugin_name = 'oracle'
plugin_desc = 'oracle reflect engine based on sqlalchemyindex, which works for many mainstream databases, including Mysql, Sqlite, etc. For mysql to work, you need to install pymysql/mysqlclient (python3) or mysql-python (python2) in advance.'
supported_ds_types = ['oracle']
required_packages = ['cx_Oracle']



ds_param = {'schema_name': {'type':'String',
                             'full_name':'Schema Name to Reflect:',
                            'default_value':'hr',
                             'desc':'',
                             },
            'connect_string': {'type':'String',
                             'full_name':'Database Connection String:',
                               'default_value': 'oracle+cx_oracle://hr:hr@192.168.1.1:1521/orcl',
                               'desc':'''The sqlalchemy access URL,  for example: oracle://root:xyz@localhost/employees.''',
                             },
            }

sample_ds_url = 'mysql://root:xyz@localhost/employees'
metadata_type='table'

author = 'duan'
class_name = 'sqlalchemyindex.SQLAlchemyReflectEngine'
notebook_template_path = 'show_sqlalchemy_table_template.ipynb'

from schemaindex.plugin.sqlalchemyindex import ReflectEngine as SqlAlchemyReflectEngine
# -----------------------------------
class ReflectEngine(SqlAlchemyReflectEngine):
    pass
#    def __init__(self,ds_dict=None, ds_name = None):
#        SqlAlchemyReflectEngine.__init__(ds_dict = ds_dict, ds_name = ds_name )
