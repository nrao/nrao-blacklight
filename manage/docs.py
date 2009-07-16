import csv

raw_docs = [record for record in csv.DictReader(open('theses.csv'))]
docs = []

# This can be simplified, but let's make it work first.
for raw_doc in raw_docs:
    doc = dict()
    for k,v in raw_doc.items():
        v = v or ''
        doc[k.lower().strip().replace(' ', '_')] = v.decode('latin1')
        doc['id'] = doc.get('primary_key', '')
    if doc.get('id', ''):
        docs.append(doc)
