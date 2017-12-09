
from hdfs import Client

from app.dbmodels import engine, MTable, MColumn, MDatabase
from app.schemaindexapp import si_app

class HDFSIndexEngine():
    ds_dict = None
    def __init__(self,ds_dict=None, ds_name = None):
        if ds_dict is not None:
            self.ds_dict = ds_dict
        elif ds_name is not None:
                self.ds_dict = si_app.get_data_source_dict(ds_name = ds_name)
        else:
            si_app.logger.error('no data source is given!')

    @staticmethod
    def echo(self):
        return 'echo'

    # get the all file information from HDFS
    def QueryHDFSFile(self, pDirectory, pClient, filelist):

        to_list_dir = pDirectory if len(pDirectory) > 1 else '/'
        tDirectoryType = pClient.status(to_list_dir).get('type')

        if tDirectoryType == 'FILE':
            filelist.append(pDirectory)

        elif tDirectoryType == 'DIRECTORY' and (not pClient.list(to_list_dir)):  # This is an empty folder
            pass
            # I skip empty directories.
        else:

            tDirectorys = pClient.list(to_list_dir)

            fileNumInFolder = 0  # the number of files in this folder
            tSubDirectorys = []
            for tDirectory in tDirectorys:
                tSubDirectory = pDirectory + '/' + tDirectory
                tSubDirectorys.append(tSubDirectory)
                if pClient.status(tSubDirectory).get('type') == 'FILE':
                    fileNumInFolder += 1

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
            print('error: db_url must be provided.')
            return

        tclient = Client(self.ds_dict['db_url'])
        path_hdfs = self.ds_dict['table_group_name']
        if path_hdfs[-1] == '/':
            # remove trailing '/' for concatenating more path
            path_hdfs = path_hdfs[:-1] #+'/'


        filelist = self.getHDFSFileInfo(tclient, path_hdfs)
        #for f in (filelist):
        #    print('*  oriPath: {}'.format(f))


        if reload_flag:
            si_app.delete_doc_from_index_by_datasource(ds_name=self.ds_dict['ds_name'])


        for t in filelist:
            print(t)

            si_app.add_table_content_index(ds_name = self.ds_dict['ds_name'],
                                           table_id=t,
                                           table_info=t,
                                           )

        # si_app.commit_index()


if __name__ == "__main__":
    adb = HDFSIndexEngine(ds_dict = { 'table_group_name': '/user/data_norm',
                                     'ds_name': 'hdfs1',
                                     'db_type':'hdfsindex',
                                     'db_url' : 'http://localhost:50070',
    })
    adb.reflect() #  None)


