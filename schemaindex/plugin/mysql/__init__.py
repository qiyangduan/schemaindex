plugin_name = 'mysql'
plugin_desc = 'mysql reflect engine based on sqlalchemyindex, you need to install pymysql/mysqlclient (python3) or mysql-python (python2) in advance.'
supported_ds_types = ['oracle']


ds_param = {'schema_name': {'type':'String',
                             'full_name':'Schema Name to Reflect:',
                            'default_value':'Not effective yet',
                             'desc':'Not effective yet',
                             },
            'connect_string': {'type':'String',
                             'full_name':'Database Connection String:',
                               'default_value': 'mysql://root:xyz@localhost/employees',
                               'desc':'''The sqlalchemy access URL.''',
                             },
            }

sample_ds_url = 'mysql://root:xyz@localhost/employees'
metadata_type='table'

author = 'duan'
# class_name = 'sqlalchemyindex.SQLAlchemyReflectEngine'
notebook_template_path = 'show_sqlalchemy_table_template.ipynb'

from schemaindex.plugin.sqlalchemyindex import ReflectEngine as SqlAlchemyReflectEngine
# -----------------------------------
class ReflectEngine(SqlAlchemyReflectEngine):
    pass
#    def __init__(self,ds_dict=None, ds_name = None):
#        SqlAlchemyReflectEngine.__init__(ds_dict = ds_dict, ds_name = ds_name )
