import csv
import user

def _docs(fd, **kwargs):
    for doc in csv.DictReader(fd):
        doc['telescope'], doc['configuration'], doc['sub'], doc['nant'] =\
            doc['tele_conf_sub_nant'].split(':')
        yield doc

docs = _docs(open('data.csv'), quotechar=None)
