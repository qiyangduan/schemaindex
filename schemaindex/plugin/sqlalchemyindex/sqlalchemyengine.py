from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, DateTime, String, Integer, ForeignKey, func
import json

from schemaindex.app.dbmodels import MTable, MColumn, MDatasource
from schemaindex.app.schemaindexapp import si_app


engine = create_engine('sqlite:///' + si_app.config['database']['sqlite_file']  )

class SQLAlchemyReflectEngine():
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

    def datasource_init(self):
        pass

    def reflect(self, reload_flag = False):
        if not self.ds_dict:
            print('error: ds_url must be provided.')
            return

        reflect_engine = create_engine(self.ds_dict['ds_param']['connect_string']   )
        metadata = MetaData(bind=reflect_engine)
        metadata.reflect()



        session = create_session(bind=engine)
        session._model_changes={}
        session.begin()

        if reload_flag:
            session.query(MTable).filter_by(ds_name = self.ds_dict['ds_name']).delete()
            session.query(MColumn).filter_by(ds_name = self.ds_dict['ds_name']).delete()
            si_app.delete_doc_from_index_by_datasource(ds_name=self.ds_dict['ds_name'])
        # tables = metadata.tables.values()
        # print(tables)



        for t in metadata.sorted_tables:
            #print(t.name)
            # t.columns.id
            # t.columns.id.comment
            session.add_all([
                MTable(
                        ds_name = self.ds_dict['ds_name'],
                        table_group_name = self.ds_dict['ds_param']['schema_name'],
                        table_name=t.name,
                        table_comment = ''
                        )
            ])


            table1 = Table(t.name, metadata
                           , autoload=True, autoload_with=engine)

            # print([c.name for c in table1.columns])
            #print([c.type for c in table1.columns])
            #print([c for c in table1.columns])
            column_list = []
            for c in table1.columns:
                # print(c)
                session.add_all([
                    MColumn(
                            ds_name = self.ds_dict['ds_name'],
                            table_name=t.name,
                            table_group_name=self.ds_dict['ds_param']['schema_name'],
                            column_name = c.name,
                            column_type = str(c.type),
                            column_comment = None # c.doc
                )
                ])
                column_list.append([c.name, str(c.type), c.doc])

            si_app.add_table_content_index(ds_name = self.ds_dict['ds_name'],
                                           table_id='/'.join(['/', self.ds_dict['ds_name'], t.name]),
                                           #info=unicode(json.dumps({"table
                                           table_info=(json.dumps({"table_group_name":  self.ds_dict['ds_param']['schema_name'],
                                                                     "ds_name":    self.ds_dict['ds_name'] ,
                                                                     "table_name":  t.name ,
                                                                     "table_comment":    ' ' ,
                                                                     "column_info": column_list
                                                                     }
                                                                    )
                                                   )
                                           )


        session.commit()
        si_app.commit_index()



if __name__ == "__main__":
    ds_dict = {
        'ds_name': 'emp1',
        'ds_type': 'hdfsindex',
        'ds_desc': 'created by unittest of hdfsindex',
        'ds_param': {'connect_string': 'mysql://root:learning@localhost/employees',
                     'schema_name': 'na',
                     }
    }


    adb = SQLAlchemyReflectEngine(ds_dict)
    adb.reflect()


