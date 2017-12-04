# from whoosh.index import create_in
from whoosh import index
from whoosh.fields import *
from whoosh.qparser import QueryParser

import config
import os


import json
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))


writer = ix.writer()


class TextIndexer():
    ix = None

    def __init__(self):
        db_type = 'mysqlflex'
        indexdir = config['main']['schemaflex_text_index_path']

        if not os.path.exists(indexdir):
            os.mkdir(indexdir)
            ix = index.create_in(indexdir, schema)  # ""
        else:
            ix = index.open_dir(indexdir)

    def write_tables(self, tables_data = None):
        if ix is None:
            print('error, ix not initialized')

        writer = ix.writer()
        for tab in tables_data:
            writer.add_document(table_name_desc=tab['table_name_desc'],
                                table_id=tab['table_name_desc'],
                                column_name_desc=tab['column_name_desc'],
                                )
        writer.commit()

    def query_tables(self, query_string=None):
        if ix is None:
            print('error, ix not initialized')

        with ix.searcher() as searcher:
            query = QueryParser("column_name_desc", ix.schema).parse("customer")
            results = searcher.search(query)
            print(results[0])

            b = json.loads(results[0]['column_name_desc'])
            print(b)

            return results
