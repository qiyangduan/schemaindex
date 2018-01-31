plugin_name = 'MS_SQL_Server'
plugin_desc = 'mssql can reflect Microsoft SQL Server engine based on sqlalchemyindex.'
supported_ds_types = ['oracle']
required_packages = ['pymssql']


ds_param = {'schema_name': {'type':'String',
                             'full_name':'Schema Name to Reflect:',
                            'default_value':'Not effective yet',
                             'desc':'Not effective yet',
                             },
            'connect_string': {'type':'String',
                             'full_name':'Database Connection String:',
                               'default_value': 'mssql+pymssql://sa:yourPassword@127.0.0.1/samd?charset=utf8',
                               'desc':'''The sqlalchemy access URL.''',
                             },
            }

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
