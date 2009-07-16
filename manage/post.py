#!/usr/bin/env python

from pysolr import Solr

from docs import docs

print len(docs)

solr_url = 'http://localhost:8983/solr'
conn = Solr(solr_url)

conn.delete(q='*:*')
conn.commit()
conn.add(docs)
conn.commit()
