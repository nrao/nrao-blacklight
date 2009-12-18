#!/usr/bin/env python

import pyfits

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
                # swfreq has an unquoted comma in it.
                if value.startswith('swfreq '):
                    value = value.replace('= ', '= "') + '"'
                if '=' in value:
                    doc.update(eval('dict(%s)' % ('config_' + value)))
                keyword, value = pointer.next()
        if value.startswith('Catalog'):
            while True:
                keyword, value = pointer.next()
                if ':' in value:
                    value = value.replace(': ', '= """') + '"""'
                    doc.update(eval('dict(%s)' % ('catalog_' + value)))
                    keyword, value = pointer.next()
    except StopIteration:
        return doc
    return doc

print build_doc('GO.fits')
