import os
import simplejson
from config import cfg
from datetime import datetime as sysdt

from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Table, Column, DateTime, String, Integer, ForeignKey, func

from whoosh.index import create_in
from whoosh.fields import *


Base = declarative_base()


from dbmodels import engine, MTable, MColumn, MDatabase


this is bad

class MysqlReflectEngine():
    def __init__(self):
        db_type = 'mysqlflex'

    def reflect_database(self, display_name, ds_name, reload_flag=True, db_url=None):
        if not db_url:
            db_url = 'sqlite:////home/duan/github/schemamap/app/allmodel.sqlite3flex'
            db_type = 'sqlite3flex'

        reflect_engine = create_engine(db_url)
        metadata = MetaData(bind=reflect_engine)
        metadata.reflect()


        session = create_session(bind=engine)
        session._model_changes={}
        session.begin()

        if reload_flag:
            session.query(MTable).delete()
            # session.commit()
        # tables = metadata.tables.values()
        # print(tables)
        for t in metadata.sorted_tables:
            print(t.name)
            # t.columns.id
            # t.columns.id.comment
            session.add_all([
                MTable(  display_name='sqlite' ,
                         ds_name = 'default',
                         table_name=t.name,
                         table_comment = ''
                        )
            ])

        connection = engine.connect()
        result = connection.execute("SELECT table_name, column_name, COLUMN_COMMENT FROM INFORMATION_SCHEMA.COLUMNS " +
                                    "WHERE TABLE_SCHEMA = 'blog'  ")
        for row in result:
            print("table name:", row['table_name'], " - ", row['column_name'], " - ", row['COLUMN_COMMENT'])
        connection.close()



        session.commit()




class SQLAlchemyReflectEngine():
    def __init__(self):
        db_type = 'sqlite3flex'
    def reflect_database(self, db_type, display_name = None, ds_name= None, reload_flag=True, db_url=None):
        if not db_url:
            #db_url = 'sqlite:////home/duan/github/schemamap/app/allmodel.sqlite3flex'
            #db_type = 'sqlite3flex'
            print('error: db_url must be provided.')

        reflect_engine = create_engine(db_url)
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

        schema = Schema(table_id=ID(stored=True), table_info=TEXT(stored=True)) # , column_info=TEXT(stored=True)
        indexdir = cfg['main']['schemaflex_text_index_path']
        ix = create_in(indexdir , schema)
        writer = ix.writer()
#        writer.add_document(table_name_desc=u'{"event": "the event table"}', table_id=u'/b',
#                            column_name_desc=u'{"event_date":"when the event happen interesting!","event_code":"the code of event, with 11 digits"}')


        for t in metadata.sorted_tables:
            print(t.name)
            # t.columns.id
            # t.columns.id.comment
            session.add_all([
                MTable(
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
            column_list = []
            for c in table1.columns:
                # print(c)
                session.add_all([
                    MColumn(
                              ds_name = ds_name,
                              table_name=t.name,
                              column_name = c.name,
                              column_type = str(c.type),
                              column_comment = None # c.doc

                )
                ])
                column_list.append([c.name, str(c.type), c.doc])

            writer.add_document(table_id='/'.join(['/',ds_name, t.name]),
                                table_info=unicode(simplejson.dumps({"ds_name":  display_name,
                                                                     "ds_name":    ds_name ,
                                                                     "table_name":  t.name ,
                                                                     "table_comment":    ' ' ,
                                                                     "column_info": column_list
                                                                     }
                                                                    )
                                                   )
                                )


        session.commit()
        writer.commit()

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
    reflect_db('blog')
