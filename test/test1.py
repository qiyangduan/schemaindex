snippet_template = '''
import pandas as pd
from hdfs import Client
tclient = Client( '$$hdfs_web_url$$')
with tclient.read('$$file_path$$', encoding='utf-8') as reader:
df=pd.read_csv(reader)
df.head()
'''
replace_dict = {'$$file_path$$': 'aaa',
                '$$hdfs_web_url$$': 'bbb'}
# snippet_result = (reduce(lambda a, kv: a.replace(*kv), replace_dict.iteritems(), snippet_template))
snippet_result = snippet_template
for key in replace_dict.keys():
    snippet_result = snippet_result.replace(key, replace_dict[key])
print(snippet_result)

