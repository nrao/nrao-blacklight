import csv
import datetime
import user

strptime = datetime.datetime.strptime

def _docs(fd, **kwargs):
    for doc in csv.DictReader(fd):
        doc['start'] = strptime(doc['start'], '%y-%b-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
        doc['stop'] = strptime(doc['stop'], '%y-%b-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
        doc['id'] = doc['project'] + '_' + doc['start']
        doc['telescope'], doc['configuration'], doc['sub'], doc['nant'] =\
            doc['tele_conf_sub_nant'].split(':')
        yield doc

docs = _docs(open('data.csv'), quotechar=None)
