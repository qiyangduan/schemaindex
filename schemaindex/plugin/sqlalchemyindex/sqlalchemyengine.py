from sqlalchemy import create_engine
from sqlalchemy.orm import create_session
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, DateTime, String, Integer, ForeignKey, func
import json
import os

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
            column_name_str = ''
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
                column_name_str = column_name_str + ', ' + c.name

            si_app.add_table_content_index(ds_name = self.ds_dict['ds_name'],
                                           table_id=t.name, #'/'.join(['/', self.ds_dict['ds_name'], t.name]),
                                           table_info=(json.dumps({ #"table_group_name":  self.ds_dict['ds_param']['schema_name'],
                                                                     # "ds_name":    self.ds_dict['ds_name'] ,
                                                                     "table_name":  t.name ,
                                                                     # "table_comment":    ' ' ,
                                                                     "column_info": column_list,
                                                                     }
                                                                    )
                                                   ),
                                           table_content_index= t.name + '  ' + column_name_str
                                           )


        session.commit()
        si_app.commit_index()

    def generate_notebook(self, schemaindex_notebooks_dir = '/tmp', table_id = None):

        spec_dir = si_app.config['main']['schemaflex_spec']
        replace_dict = {'$$TABLE$$': table_id,
                        '$$connect_string$$': self.ds_dict['ds_param']['connect_string']}
        generated_loc = os.path.join(spec_dir,'hdfsindex', 'show_table_%s_%s.ipynb' %
                                     (self.ds_dict['ds_name'], table_id.replace('/','_') )          )
        with open(os.path.join(spec_dir,'sqlalchemyindex', 'show_sqlalchemy_table_template.ipynb'), "rt") as fin:
            with open( generated_loc, "wt") as fout:
                for line in fin:
                    # fout.write(line.replace('$$TABLE$$', table_name))
                    snippet_result = line
                    for key in replace_dict.keys():
                        snippet_result = snippet_result.replace(key, replace_dict[key])

                    # fout.write(reduce(lambda a, kv: a.replace(*kv), replace_dict.iteritems(), line))
                    fout.write(snippet_result)

        return generated_loc

    def generate_notebook_snippet(self, table_id = None):

        snippet_template = '''
#!pip install pandas        
from sqlalchemy import create_engine
import pandas as pd

ds_url = '$$connect_string$$'
engine = create_engine(ds_url)
conn = engine.connect()
# for quick glance, append Oracle:  ' where rownum < 3' , Mysql/sqlite: ' limit 10'
df = pd.read_sql('select * from $$TABLE$$', con=conn)
df.head()
'''
        replace_dict = {'$$TABLE$$': table_id,
                        '$$connect_string$$': self.ds_dict['ds_param']['connect_string']}
        # snippet_result = (reduce(lambda a, kv: a.replace(*kv), replace_dict.iteritems(), snippet_template))
        snippet_result = snippet_template
        for key in replace_dict.keys():
            snippet_result = snippet_result.replace(key, replace_dict[key])

        # print(snippet_result)
        return snippet_result

if __name__ == "__main__":
    ds_dict = {
        'ds_name': 'emp1',
        'ds_type': 'hdfsindex',
        'ds_desc': 'created by unittest of hdfsindex',
        'ds_param': {'connect_string': 'mysql://root:xxx@localhost/employees',
                     'schema_name': 'na',
                     }
    }


    adb = SQLAlchemyReflectEngine(ds_dict)
    adb.reflect()


