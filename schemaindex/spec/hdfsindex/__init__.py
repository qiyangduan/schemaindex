plugin_name = 'hdfsindex'

plugin_desc = 'Given the connection information and initial path, this plugin recursively scan through all files in a HDFS system and index them.'
supported_ds_types = ['HDFS']

sample_ds_url = 'http://localhost:50070'
author = 'duan'

class_name = 'a.b'

from .hdfsindexengine import HDFSIndexEngine as ReflectEngine
