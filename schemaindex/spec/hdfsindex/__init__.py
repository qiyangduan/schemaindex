plugin_name = 'hdfsindex'

plugin_desc = '''Given the connection information and initial path, this plugin recursively scan through all files in a HDFS system and index them. 
The index schema is Schema(ds_name=ID(stored=True), table_id=ID(stored=True), table_info=TEXT(stored=True)) .
The real time index engine requires the hdfs connection information.'''
supported_ds_types = ['HDFS']

sample_ds_url = 'http://localhost:50070'
author = 'duan'
notebook_template_path = 'show_hdfs_file_template.ipynb'

class_name = 'a.b'

from .hdfsindexengine import HDFSIndexEngine as ReflectEngine
