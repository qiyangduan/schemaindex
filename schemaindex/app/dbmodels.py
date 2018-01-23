import os
import json
from copy import deepcopy

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from sqlalchemy import Column, DateTime, String, Integer, func

Base = declarative_base()


class MPlugin(Base):
    __tablename__ =  'mplugin'
    plugin_name = Column(String(100), primary_key=True,)
    module_name = Column(String(1200))
    metadata_type = Column(String(120), default='table')
    # plugin_status = Column(String(200))
    plugin_spec_path = Column(String(200))
    notebook_template_path = Column(String(500))
    ds_param  = Column(String(4000)) #Customized parameter by each plugin, stored as a python dict object in json string.
    supported_ds_types = Column(String(200))
    sample_ds_url = Column(String(1000))
    author = Column(String(200))
    created_date = Column(DateTime, default=func.now())
    plugin_desc = Column(String(1000))
    def __repr__(self):
        return "<pluggin (name='%s', path='%s' )>" % (
            self.plugin_name, self.plugin_spec_path )


#Reflect each database table we need to use, using metadata
class MDatasource(Base):
    __tablename__ =  'mdatasource'
    #db_id = Column(Integer, primary_key=True, autoincrement=True)
    ds_name = Column(String(100), primary_key=True,)
    # db_trx_id = Column(Integer, default=-2) # This is to track current datasource id if it is sychonized in real time. For example, hdfs inotify txid
    nbr_of_tables = Column(Integer)
    nbr_of_columns = Column(Integer)
    ds_type = Column(String(100) )
    # ds_url = Column(String(1000))
    # table_group_name = Column(String(200), default='_NA')
    created_date = Column(DateTime, default=func.now())
    last_reflect_date = Column(DateTime)
    ds_param  = Column(String(4000)) #Customized parameter by each plugin, stored as a python dict object in json string.
    ds_desc = Column(String(1000))
    ds_tags = Column(String(2550))
    def __repr__(self):
        return "<database (name='%s', ds_type = %s,   last_reflect_date='%s')>" % (
            self.ds_name, self.ds_type,   self.last_reflect_date)


    @staticmethod
    def from_dict(ds_dict=None):
        ds =     MDatasource(# table_group_name=ds_dict['table_group_name'],
                             ds_name=ds_dict['ds_name'],
                             ds_type=ds_dict['ds_type'],
                             # ds_url=ds_dict['ds_url'],
                             ds_param=json.dumps(ds_dict['ds_param']),
                             nbr_of_tables=0,
                             nbr_of_columns=9,
                             ds_desc=ds_dict['ds_desc'] if 'ds_desc' in ds_dict.keys() else '',
                             created_date=func.now(),
                             )
        return ds


    def to_dict(self):
        ds_dict = deepcopy(self.__dict__)
        ds_dict['ds_param'] = json.loads(ds_dict['ds_param'])
        return ds_dict


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
