# See example.docs.py.

import csv
import datetime
import pytz
import user

raw_docs = [record for record in csv.DictReader(open('data.csv'), escapechar='\\')]
docs = []

def get_utc_datetime(timestamp, format='%Y-%m-%d %H:%M:%S', tz='US/Eastern'):
    timezone = pytz.timezone(tz)
    utc = pytz.utc
    dt = datetime.datetime.strptime(timestamp, format)
    return timezone.localize(dt).astimezone(utc)

# This can be simplified, but let's make it work first.
for raw_doc in raw_docs:
    doc = dict()
    for k,v in raw_doc.items():
        v = v or ''
        doc[k.lower().strip().replace(' ', '_')] = v.decode('utf8')
    doc['id'] = doc.get('filename', '')
    doc['year'] = doc.pop('procyear', '')
    doc['pagenumbers'] = str(doc.get('firstpage', ''))
    if doc.get('modified', ''):
        doc['modified'] = get_utc_datetime(doc['modified'])
    if doc.get('created', ''):
        doc['created'] = get_utc_datetime(doc['created'])
    if int(doc.get('lastpage', '0')) > 0:
        doc['pagenumbers'] = '%s-%s' % (doc['pagenumbers'], doc['lastpage'])
    doc['pagenumbers'].strip('-')
    if doc.get('id', ''):
        docs.append(doc)
