#!/usr/bin/env python

import sys

from pysolr import Solr

from docs import docs

solr_url = 'http://localhost:8996/solr'
print 'connecting to Solr at', solr_url

conn = Solr(solr_url)

if '-d' in sys.argv:
    print 'deleting docs in Solr'
    conn.delete(q='*:*')
    conn.commit()
else:
    print "use flag '-d' to delete all Solr docs before adding docs"

print 'adding docs to Solr (interrupt as needed)'
count = 0
try:
    for doc in docs:
        conn.add([doc])
        count += 1
except KeyboardInterrupt:
    print
    print count, 'docs'
conn.commit()
