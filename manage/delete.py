#!/usr/bin/env python

from pysolr import Solr

solr_url = 'http://localhost:8994/solr'
print 'connecting to Solr at', solr_url

conn = Solr(solr_url)
print 'deleting docs in Solr'
conn.delete(q='*:*')
conn.commit()
