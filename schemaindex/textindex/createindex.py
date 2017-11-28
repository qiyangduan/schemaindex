from whoosh.index import create_in
from whoosh.fields import *
import simplejson as json
schema = Schema(table_name_desc=TEXT(stored=True), table_id=ID(stored=True), column_name_desc=TEXT(stored=True))
ix = create_in("indexdir", schema)
writer = ix.writer()
writer.add_document(table_name_desc=u'{"customer": "table customer"}', table_id=u'/a',
                    column_name_desc=u'{"cust_name": "this is the name of the customer", "age":"age of customer"}')
writer.add_document(table_name_desc=u'{"event": "the event table"}', table_id=u'/b',
                    column_name_desc=u'{"event_date":"when the event happen interesting!","event_code":"the code of event, with 11 digits"}')
writer.commit()




