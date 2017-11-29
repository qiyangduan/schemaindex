import os

from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import create_session

import config

Base = declarative_base()
from sqlalchemy import Column, DateTime, String, Integer, func

Base = declarative_base()


class MPlugin(Base):
    __tablename__ =  'mplugin'
    plugin_name = Column(String(100), primary_key=True,)
    module_name = Column(String(1200))
    # plugin_status = Column(String(200))
    plugin_spec_path = Column(String(200))
    supported_ds_types = Column(String(200))
    sample_ds_url = Column(String(1000))
    author = Column(String(200))
    created_date = Column(DateTime, default=func.now())
    plugin_desc = Column(String(1000))
    def __repr__(self):
        return "<pluggin (name='%s', path='%s' )>" % (
            self.ds_type_name, self.full_path )


#Reflect each database table we need to use, using metadata
class MDatabase(Base):
    __tablename__ =  'mdatabase'
    #db_id = Column(Integer, primary_key=True, autoincrement=True)
    ds_name = Column(String(100), primary_key=True,)
    table_group_name = Column(String(200), default='_NA')
    nbr_of_tables = Column(Integer)
    nbr_of_columns = Column(Integer)
    created_date = Column(DateTime, default=func.now())
    last_reflect_date = Column(DateTime, default=func.now())
    db_type = Column(String(100) )
    db_url = Column(String(1000))
    db_comment = Column(String(1000))
    db_desc = Column(String(1000))
    db_tags = Column(String(2550))
    def __repr__(self):
        return "<database (name='%s', db_url='%s', last_reflect_date='%s')>" % (
            self.table_group_name, self.db_url, self.last_reflect_date)

class MTable(Base):
    __tablename__ = 'mtable'
    # table_id = Column(Integer, primary_key=True, autoincrement=True)
    # db_id = Column(Integer)
    ds_name = Column(String(100), primary_key=True,)
    table_group_name = Column(String(200), default='_NA')
    table_name = Column(String(255), primary_key=True)
    table_type = Column(String(255))
    table_comment = Column(String(5000))

#Reflect each database table we need to use, using metadata
class MColumn(Base):
    __tablename__ =  'mcolumn'
    # table_id = Column(Integer, primary_key=True)
    ds_name = Column(String(100), primary_key=True,)
    table_group_name = Column(String(200), default='_NA')
    table_name = Column(String(255), primary_key=True)
    column_name = Column(String(255), primary_key=True)
    column_seq = Column(Integer)
    column_type = Column(String(255))
    column_comment = Column(String(1000))
    column_tags = Column(String(2550))

db_file_path = os.path.join(os.getcwd(), config.cfg['database']['sqlite_file'])
engine = create_engine('sqlite:///' + db_file_path)

if __name__ == "__main__":
    # insert_initial_stanmo_data()

    engine = create_engine('sqlite:////home/duan/github/schemamap/app/allmodel.sqlite3flex')
    metadata = MetaData(bind=engine)
    metadata.reflect()
    # tables = metadata.tables.values()
    # print(tables)
    for t in metadata.sorted_tables:
        print(t.name)
        # t.columns.id
        # t.columns.id.comment
'''
    connection = engine.connect()
    result = connection.execute("SELECT table_name, column_name, COLUMN_COMMENT FROM INFORMATION_SCHEMA.COLUMNS " +
                                "WHERE TABLE_SCHEMA = 'blog'  ")
    for row in result:
        print("username:", row['table_name'], " - ", row['column_name'], " - ", row['COLUMN_COMMENT'])
    connection.close()

from sqlalchemyflex import MetaData,create_engine

# default
#engine = create_engine('mysqlflex://scott:tiger@localhost/foo')
# engine = create_engine('sqlite:////home/duan/github/jupyter/schema_display/c.db')


# mysqlflex-python
#engine = create_engine('mysqlflex+mysqldb://scott:tiger@localhost/foo')

# MySQL-connector-python
#engine = create_engine('mysqlflex+mysqlconnector://scott:tiger@localhost/foo')

# OurSQL
#engine = create_engine('mysqlflex+oursql://scott:tiger@localhost/foo')

# create the pydot graph object by autoloading all tables via a bound metadata object
# metadata=MetaData('sqlite:////home/duan/github/jupyter/schema_display/c.db')
engine = create_engine('mysqlflex://root:x@localhost/blog')
metadata=MetaData('mysqlflex://root:x@localhost/blog')

metadata.reflect()
#tables = metadata.tables.values()
#print(tables)
for t in metadata.sorted_tables:
    print(t.name)
    # t.columns.id
    # t.columns.id.comment

connection = engine.connect()
result = connection.execute("SELECT table_name, column_name, COLUMN_COMMENT FROM INFORMATION_SCHEMA.COLUMNS " +
                            "WHERE TABLE_SCHEMA = 'blog'  ")
for row in result:
    print("table name:", row['table_name'], " - ", row['column_name'], " - ", row['COLUMN_COMMENT']  )
connection.close()

'''


