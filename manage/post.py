#!/usr/bin/env python

import sys

from pysolr import Solr

from docs import docs

print 'number of docs:', len(docs)

solr_url = 'http://localhost:8991/solr'
print 'connecting to Solr at', solr_url

conn = Solr(solr_url)

if '-d' in sys.argv:
    print 'deleting docs in Solr'
    conn.delete(q='*:*')
    conn.commit()
else:
    print "use flag '-d' to delete all Solr docs before adding docs"

print 'adding docs to Solr'
conn.add(docs)
conn.commit()
