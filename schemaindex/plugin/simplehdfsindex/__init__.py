import os
import json
import subprocess
import datetime

from hdfs import Client

from schemaindex.app.schemaindexapp import si_app

# -----------------------------------
plugin_name = 'simplehdfsindex'
plugin_desc = '''Given the connection information and initial path, this plugin recursively scan through all files in a HDFS system and index them. '''
required_packages = ['hdfs']

ds_param = {'hdfs_web_url': {'type':'String',
                             'full_name':'HDFS Web URL (Required):',
                             'default_value': 'http://localhost:50070',
                             'desc':'''The HDFS web URL, usually staring with HTTP, for example: http://localhost:50070 .  This URL is used by hdfscli library to connect to HDFS web and scan HDFS structure.''',
                             },
            'root_path': {'type':'String',
                             'full_name':'Root path (Required):',
                             'default_value': '/',
                             'desc':'The starting point to index for the index, for example, you can use / or /user', #
                             },

            }


_________ds_param_desc = {'hdfs_web_url': '''The HDFS web URL, usually staring with HTTP, for example: http://localhost:50070 .  This URL is used by hdfscli library to connect to HDFS web and scan HDFS structure.''',
            'root_path': 'The starting point to index for the index', # Sample: /
            }


supported_ds_types = ['HDFS']
metadata_type='file'

sample_ds_url = 'http://localhost:50070'
author = 'duan'
notebook_template_path = 'show_hdfs_file_template.ipynb'



# -----------------------------------
class ReflectEngine():
    ds_dict = None
    si_app = None

    def __init__(self,si_app = None, ds_dict=None, ds_name = None):
        self.si_app = si_app
        if ds_dict is not None:
            self.ds_dict = ds_dict
        elif ds_name is not None:
                self.ds_dict = si_app.get_data_source_dict(ds_name = ds_name)
        else:
            si_app.logger.error('no data source is given!')
            return

    # get the all file information from HDFS
    def QueryHDFSFile(self, pDirectory, pClient, filelist):

        to_list_dir = pDirectory if len(pDirectory) > 1 else '/'
        tDirectoryStatus = pClient.status(to_list_dir)
        tDirectoryType = tDirectoryStatus.get('type')

        if tDirectoryType == 'FILE':
            formatted_time = datetime.datetime.fromtimestamp(int(tDirectoryStatus.get('modificationTime')) / 1000
                                                             ).strftime(si_app.TIME_FORMATER)
            fileDict = {
                'table_name':pDirectory,
                'modificationTime':   formatted_time   ,
                'length': tDirectoryStatus.get('length'),
            }
            filelist.append(fileDict)

        elif tDirectoryType == 'DIRECTORY' and (not pClient.list(to_list_dir)):  # This is an empty folder
            pass
            # I skip empty directories.
        else:

            tDirectorys = pClient.list(to_list_dir)

            #fileNumInFolder = 0  # the number of files in this folder
            tSubDirectorys = []
            for tDirectory in tDirectorys:
                tSubDirectory = pDirectory + '/' + tDirectory
                tSubDirectorys.append(tSubDirectory)
                #if pClient.status(tSubDirectory).get('type') == 'FILE':
                #    fileNumInFolder += 1

            for tSubDirectory in tSubDirectorys:
                self.QueryHDFSFile(tSubDirectory, pClient, filelist)

    # get the all file information from HDFS
    def getHDFSFileInfo(self,tclient, pInitDir):
        filelist = []
        # if pInitDir is a file, fileNum = 1; if pInitDir is a directory, fileNum here has no influence
        self.QueryHDFSFile(pInitDir, tclient, filelist)
        return filelist

    def reflect(self, reload_flag = False):
        if not self.ds_dict:
            si_app.logger.error('error: ds_dict must be provided.')
            return

        if reload_flag:
            si_app.delete_doc_from_index_by_datasource(ds_name=self.ds_dict['ds_name'])


        tclient = Client( self.ds_dict['ds_param']['hdfs_web_url'])     # self.ds_dict['ds_url'])
        path_hdfs = self.ds_dict['ds_param']['root_path']      # self.ds_dict['table_group_name']

        if path_hdfs[-1] == '/':
            # remove trailing '/' for concatenating more path
            path_hdfs = path_hdfs[:-1] # remove the trailing '/'

        filelist = self.getHDFSFileInfo(tclient, path_hdfs)


        for fd in filelist:
            si_app.add_table_content_index(ds_name = self.ds_dict['ds_name'],
                                           table_id=fd['table_name'],
                                           table_info=(json.dumps(fd) ),
                                           table_content_index = ' '.join([fd[k] for k in fd.keys() ])
                                           )
        # ds_dict = si_app.get_data_source_dict(ds_name=self.ds_dict['ds_name'])

    def datasource_init(self):
        pass


    def generate_notebook(self, schemaindex_notebooks_dir = '/tmp', table_id = None):

        spec_dir = si_app.config['main']['schemaflex_spec']
        replace_dict = {'$$file_path$$': table_id,
                        '$$hdfs_web_url$$': self.ds_dict['ds_param']['hdfs_web_url']}
        generated_loc = os.path.join(spec_dir,'hdfsindex', 'show_hdfs_file_%s_%s.ipynb' %
                                     (self.ds_dict['ds_name'], table_id.replace('/','_') )          )
        with open(os.path.join(spec_dir,'hdfsindex', 'show_hdfs_file_template.ipynb'), "rt") as fin:
            with open( generated_loc, "wt") as fout:
                for line in fin:
                    snippet_result = line
                    for key in replace_dict.keys():
                        snippet_result = snippet_result.replace(key, replace_dict[key])

                    fout.write(snippet_result)
        return generated_loc

    def generate_notebook_snippet(self, table_id = None):

        snippet_template = '''
#!pip install pandas        
import pandas as pd
from hdfs import Client
tclient = Client( '$$hdfs_web_url$$')
with tclient.read('$$file_path$$', encoding='utf-8') as reader:
  df=pd.read_csv(reader)
df.head()
'''
        replace_dict = {'$$file_path$$': table_id,
                        '$$hdfs_web_url$$': self.ds_dict['ds_param']['hdfs_web_url']}
        # snippet_result = (reduce(lambda a, kv: a.replace(*kv), replace_dict.iteritems(), snippet_template))
        snippet_result = snippet_template
        for key in replace_dict.keys():
            snippet_result = snippet_result.replace(key, replace_dict[key])

        # print(snippet_result)
        return snippet_result

if __name__ == "__main__":
    ds_dict = {
        'ds_name': 'hdfs2',
        'ds_type': 'simplehdfsindex',
        'ds_desc': 'created by unittest of hdfsindex',
        'ds_url': 'http://localhost:50070',
        'ds_param': {'hdfs_web_url': 'http://localhost:50070' ,
                     'root_path': '/',
                     }
    }

    si_app.add_data_soruce(ds_dict)
    a = ReflectEngine(ds_dict = ds_dict)
    a.reflect()



