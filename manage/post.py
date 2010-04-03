#!/usr/bin/env python

import sys

from pysolr import Solr

from docs import docs

solr_url = 'http://localhost:8994/solr'
print 'connecting to Solr at', solr_url

conn = Solr(solr_url, timeout=3600)

if '-d' in sys.argv:
    print 'deleting docs in Solr'
    conn.delete(q='*:*')
    conn.commit()
else:
    print "use flag '-d' to delete all Solr docs before adding docs"

print 'adding docs to Solr'
count = 0
# Using a generator, for lazy loading.
try:
    for doc in docs:
        if doc.get('error'):
            print
            print doc.get('id')
            print doc['error']
            print
            _ = raw_input()
        if not (doc and doc.get('id')):
            sys.stdout.write('-')
            sys.stdout.flush()
            continue
        conn.add([doc], commit=False)
        count += 1
        sys.stdout.write('.')
        sys.stdout.flush()
except KeyboardInterrupt:
    pass
finally:
    print
    print 'committing docs'
    sys.stdout.flush()
    conn.commit()
    print
    print 'Number of docs:', count
