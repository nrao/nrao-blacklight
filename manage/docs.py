# See example.docs.py.

import csv
import datetime

raw_docs = [record for record in csv.DictReader(open('data.csv'), escapechar='\\')]
docs = []

# This can be simplified, but let's make it work first.
for raw_doc in raw_docs:
    doc = dict()
    for k,v in raw_doc.items():
        v = v or ''
        doc[k.lower().strip().replace(' ', '_')] = v.decode('latin1')
    doc['id'] = doc.get('filename', '')
    doc['year'] = doc.pop('procyear', '')
    doc['pagenumbers'] = str(doc.get('firstpage', ''))
    if doc.get('modified', ''):
        m = doc['modified']
        doc['modified'] = datetime.datetime.strptime(m, '%Y-%m-%d %H:%M:%S')
    if doc.get('created', ''):
        c = doc['created']
        doc['created'] = datetime.datetime.strptime(c, '%Y-%m-%d %H:%M:%S')
    if int(doc.get('lastpage', '0')) > 0:
        doc['pagenumbers'] = '%s-%s' % (doc['pagenumbers'], doc['lastpage'])
    doc['pagenumbers'].strip('-')
    if doc.get('id', ''):
        docs.append(doc)
