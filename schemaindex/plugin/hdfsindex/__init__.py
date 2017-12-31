plugin_name = 'hdfsindex'
plugin_desc = '''Given the connection information and initial path, this plugin recursively scan through all files in a HDFS system and index them. 
The index schema is Schema(ds_name=ID(stored=True), table_id=ID(stored=True), table_info=TEXT(stored=True)) .
The real time index engine requires the hdfs connection information.'''

ds_param = {'hdfs_web_url': {'type':'String',
                             'full_name':'HDFS Web URL (Required):',
                             'desc':'''The HDFS web URL, usually staring with HTTP, for example: http://localhost:50070 .  This URL is used by hdfscli library to connect to HDFS web and scan HDFS structure.''',
                             },
            'hdfs_url': {'type':'String',
                             'full_name':'HDFS Native URI for inotify:',
                             'desc':'''The HDFS native access URL, usually staring with hdfs, for example: hdfs://localhost:9000 . This URL is used by a Java inotify library to connect to HDFS and monitor all file level changes to HDFS.''',
                             },
            'root_path': {'type':'String',
                             'full_name':'Root path (Required):',
                             'desc':'The starting point to index for the index, for example, you can use / or /user', #
                             },
            'start_inotify':{'type':'Boolean',
                             'full_name':'Start real time inotify synchronization',
                             'desc':'Whether to continously monitor the HDFS changes, or Not.'  # False
                             },
            'inotify_trx_id':{'type':'String',
                             'full_name':'Starting transaction id for Hadoop inotify:',
                             'desc':'-1 to Start from the end and 0 to start from beginning.'  # False
                             },

            }

'''
ds_param = {'hdfs_web_url': 'String', # Sample: http://localhost:50070
            'hdfs_url': 'String', # Sample: hdfs://localhost:9000
            'root_path': 'String', # Sample: /
            'start_inotify':'Boolean'  # False
            }
'''

ds_param_desc = {'hdfs_web_url': '''The HDFS web URL, usually staring with HTTP, for example: http://localhost:50070 .  This URL is used by hdfscli library to connect to HDFS web and scan HDFS structure.''',
            'hdfs_url': '''The HDFS native access URL, usually staring with hdfs, for example: hdfs://localhost:9000 . This URL is used by a Java inotify library to connect to HDFS and monitor all file level changes to HDFS.''',
            'root_path': 'The starting point to index for the index', # Sample: /
            'start_inotify':'Whether to continously monitor the HDFS changes, or Not.'  # False
            }


supported_ds_types = ['HDFS']

sample_ds_url = 'http://localhost:50070'
author = 'duan'
notebook_template_path = 'show_hdfs_file_template.ipynb'

class_name = 'a.b'

from .hdfsindexengine import HDFSIndexEngine as ReflectEngine
