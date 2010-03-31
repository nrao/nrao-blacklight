import sys

from docs import doc_id

# Run through a listing of projects in the archive, trying out proposal ID.
for line in open('projects.txt'):
    name = line.strip()
    record = {'PROJID': name, 'SCAN': '001'}
    prop_id = doc_id(record)
    if prop_id:
        print '%s -> %s' % (name, prop_id)
    else:
        print >>sys.stderr, 'No ID for', name
