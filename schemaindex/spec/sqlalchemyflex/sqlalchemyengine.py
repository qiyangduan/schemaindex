from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, DateTime, String, Integer, ForeignKey, func
import simplejson as json

from app.dbmodels import engine, MTable, MColumn, MDatabase
from  app.schemaindexapp import si_app

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

    def reflect(self, reload_flag = False):
        if not self.ds_dict:
            print('error: db_url must be provided.')
            return

        reflect_engine = create_engine((self.ds_dict['db_url']))
        metadata = MetaData(bind=reflect_engine)
        metadata.reflect()

        session = create_session(bind=engine)
        session._model_changes={}
        session.begin()

        if reload_flag:
            session.query(MTable).filter_by(ds_name = self.ds_dict['ds_name']).delete()
            session.query(MColumn).filter_by(ds_name = self.ds_dict['ds_name']).delete()
        # tables = metadata.tables.values()
        # print(tables)



        for t in metadata.sorted_tables:
            print(t.name)
            # t.columns.id
            # t.columns.id.comment
            session.add_all([
                MTable(
                        ds_name = self.ds_dict['ds_name'],
                        table_group_name = self.ds_dict['table_group_name'],
                        table_name=t.name,
                        table_comment = ''
                        )
            ])


            table1 = Table(t.name, metadata
                           , autoload=True, autoload_with=engine)

            print([c.name for c in table1.columns])
            print([c.type for c in table1.columns])
            print([c for c in table1.columns])
            column_list = []
            for c in table1.columns:
                # print(c)
                session.add_all([
                    MColumn(
                            ds_name = self.ds_dict['ds_name'],
                            table_name=t.name,
                            table_group_name=self.ds_dict['table_group_name'],
                            column_name = c.name,
                            column_type = str(c.type),
                            column_comment = None # c.doc

                )
                ])
                column_list.append([c.name, str(c.type), c.doc])

            si_app.add_table_content_index(table_id='/'.join(['/', self.ds_dict['ds_name'], t.name]),
                                           table_info=unicode(json.dumps({"ds_name":  self.ds_dict['table_group_name'],
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


    @staticmethod
    def reflect_db(ds_name = None):
        session = create_session(bind=engine)
        dbrs = session.query(MDatabase).filter_by(ds_name = ds_name)
        for row in dbrs:
            adb = SQLAlchemyReflectEngine()
            adb.reflect(table_group_name = row.table_group_name,
                                    ds_name = row.ds_name,
                                    db_type=row.db_type,
                                    db_url = row. db_url
                                 )


if __name__ == "__main__":
    adb = SQLAlchemyReflectEngine(ds_dict = { 'table_group_name': 'a',
                                     'ds_name': 'a',
                                     'db_type':'sqlalchemy',
                                     'db_url' : 'mysql://root:learning@localhost/blog',
    })
    adb.reflect() #  None)


