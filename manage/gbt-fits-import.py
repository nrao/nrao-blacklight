#!/usr/bin/env python

from os.path import join, basename

import glob
import sys

import pyfits
import pysolr

keys = [] # diagnostic

def build_doc(go_path):
    doc = {}
    hdulist = pyfits.open(go_path)
    if len(hdulist) < 1:
        return doc
    header = hdulist[0].header
    pointer = iter(header.items())
    try:
        keyword, value = pointer.next()
        while keyword != 'HISTORY':
            doc[keyword] = value
            keyword, value = pointer.next()
        if value.startswith('Configuration'):
            keyword, value = pointer.next()
            while not value.startswith('Catalog'):
                if '=' in value:
                    name, datum = value.split('=', 1)
                    name = name.strip().replace('.', '_')
                    datum = ('"""' + datum
                             .strip()
                             .replace('"', '')
                             .replace("'", '')
                             + '"""'
                             )
                    doc.update(eval('dict(config_%s=%s)' % (name, datum)))
                keyword, value = pointer.next()
        if value.startswith('Catalog'):
            while True:
                keyword, value = pointer.next()
                if ':' in value:
                    name, datum = value.split(':', 1)
                    name = name.strip().replace('.', '_')
                    datum = ('"""' + datum
                             .strip()
                             .replace('"', '')
                             .replace("'", '')
                             + '"""'
                             )
                    doc.update(eval('dict(catalog_%s=%s)' % (name, datum)))
                keyword, value = pointer.next()
    except StopIteration:
        return doc
    return doc

def gather_project(project_path):
    doc = {}
    for go_path in glob.glob(join(project_path, 'GO', '*')):
        partial = build_doc(go_path)
        for k,v in partial.items():
            vs = doc.get(k, [])
            if v not in vs:
                vs.append(v)
            doc[k] = vs
    for k,v in doc.items():
        doc[k] = sorted(v)
        if k not in keys:
            keys.append(k) # diagnostic
    if doc:
        doc['id'] = basename(project_path)
        doc['keys'] = sorted(doc.keys()) # diagnostic
    return doc

if len(sys.argv) < 2:
    project_paths = glob.glob('*')
else:
    project_paths = sys.argv[1:]

solr = pysolr.Solr('http://perseus.cv.nrao.edu:8994/solr')

try:
    for project_path in project_paths:
        print >>sys.stderr, project_path
        doc = gather_project(project_path)
        if doc:
            solr.add([doc])
except KeyboardInterrupt:
    pass

solr.commit()

for key in sorted(keys):
    print key
