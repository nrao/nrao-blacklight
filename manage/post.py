#!/usr/bin/env python

from pysolr import Solr

from docs import docs

solr_url = 'http://avalon.cv.nrao.edu:8983/solr'
conn = Solr(solr_url)

conn.delete(q='*:*')
conn.commit()
conn.add(docs)
