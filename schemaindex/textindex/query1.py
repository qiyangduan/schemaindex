from whoosh import index
from whoosh.qparser import QueryParser
import simplejson as json
ix = index.open_dir("indexdir")
with ix.searcher() as searcher:
    query = QueryParser("column_name_desc", ix.schema).parse("customer")
    results = searcher.search(query)
    print(results[0])

    b=json.loads(results[0]['column_name_desc'])
    print(b)

