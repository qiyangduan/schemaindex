from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, DateTime, String, Integer, ForeignKey, func

from app.dbmodels import engine, MTable, MColumn, MDatabase
import app.schemaindexapp as si_app

class SQLAlchemyReflectEngine():
    ds_dict = None
    def __init__(self,ds_dict=None, ds_name = None):
        if ds_dict is not None:
            self.ds_dict = ds_dict



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
            session.query(MTable).filter_by(ds_name = ds_name).delete()
            session.query(MColumn).filter_by(ds_name = ds_name).delete()
            # session.commit()
        # tables = metadata.tables.values()
        # print(tables)
        for t in metadata.sorted_tables:
            print(t.name)
            # t.columns.id
            # t.columns.id.comment
            session.add_all([
                MTable(  display_name=display_name ,
                         ds_name = ds_name,
                         table_name=t.name,
                         table_comment = ''
                        )
            ])

            table1 = Table(t.name, metadata
                           , autoload=True, autoload_with=engine)

            print([c.name for c in table1.columns])
            print([c.type for c in table1.columns])
            print([c for c in table1.columns])
            for c in table1.columns:
                # print(c)
                session.add_all([
                    MColumn(  display_name=display_name ,
                              ds_name = ds_name,
                              table_name=t.name,
                              column_name = c.name,
                              column_type = str(c.type),
                              column_comment = None # c.doc

                )
                ])
        session.commit()

    @staticmethod
    def reflect_db(ds_name = None):
        session = create_session(bind=engine)
        dbrs = session.query(MDatabase).filter_by(ds_name = ds_name)
        for row in dbrs:
            adb = SQLAlchemyReflectEngine()
            adb.reflect_database(display_name = row.display_name,
                                    ds_name = row.ds_name,
                                    db_type=row.db_type,
                                    db_url = row. db_url
                                 )


if __name__ == "__main__":
    adb = SQLAlchemyReflectEngine()
    adb.reflect_database(display_name = 'db1',
                            ds_name = 'blog',
                            db_type='mysql',
                            db_url = 'mysql://root:x@localhost/blog' ) #  None)


