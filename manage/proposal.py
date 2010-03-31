# proposal - load lookup table from proposals.dat & provide project name lookup

import cPickle

lookup = cPickle.load(open('proposals.dat', 'r'))

def get(project_name):
    return lookup.get(project_name, None)
