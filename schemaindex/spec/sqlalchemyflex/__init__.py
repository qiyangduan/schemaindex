plugin_name = 'sqlalchemy'
plugin_desc = 'mysql ReflectEngine'
supported_ds_types = ['mysql','sqlite3']


ds_param = {'schema_name': {'type':'String',
                             'desc':'''''',
                             },
            'ds_url': {'type':'String',
                             'desc':'''The HDFS native access URL, usually staring with hdfs, for example: hdfs://localhost:9000 . This URL is used by a Java inotify library to connect to HDFS and monitor all file level changes to HDFS.''',
                             },
            }


sample_ds_url = 'mysql://root:xyz@localhost/employees'

author = 'duan'
class_name = 'sqlalchemyflex.SQLAlchemyReflectEngine'
notebook_template_path = 'show_sqlalchemy_table_template.ipynb'

from .sqlalchemyengine import SQLAlchemyReflectEngine as ReflectEngine
