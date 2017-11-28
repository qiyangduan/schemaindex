from whoosh.index import create_in
from whoosh.fields import *
import simplejson as json
schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
ix = create_in("indexdir", schema)
writer = ix.writer()
writer.add_document(title=u'First document', path=u'/a',
                    content=u'{"cust_name": "this is the name of the customer", "age":"age of customer"}')
writer.add_document(title=u'Second document', path=u'/b',
                    content=u'{"event_date":"when the event happen interesting!","event_code":"the code of event, with 11 digits"}')
writer.commit()
from whoosh.qparser import QueryParser
with ix.searcher() as searcher:
    query = QueryParser("content", ix.schema).parse("customer")
    results = searcher.search(query)
    print(results[0])

    b=json.loads(results[0]['content'])
    print(b)



