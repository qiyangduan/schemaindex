plugin_name = 'sqlalchemy'

plugin_desc = 'mysql ReflectEngine'
supported_ds_types = ['mysql','sqlite3']

sample_ds_url = 'mysql://root:xyz@localhost/employees'
author = 'duan'

class_name = 'sqlalchemyflex.SQLAlchemyReflectEngine'
notebook_template_path = 'show_sqlalchemy_table_template.ipynb'

from .sqlalchemyengine import SQLAlchemyReflectEngine as ReflectEngine
