import csv
import datetime
import user

strptime = datetime.datetime.strptime

def _docs(fd, **kwargs):
    ids = set()
    for doc in csv.DictReader(fd):
        candidate_id = doc['project'] + strptime(doc['start'], '%y-%b-%d %H:%M:%S').strftime('_%Y-%m-%d_%H:%M:%S')
        doc['start'] = strptime(doc['start'], '%y-%b-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
        doc['stop'] = strptime(doc['stop'], '%y-%b-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%SZ')
        doc['id'] = candidate_id
        count = 1
        while doc['id'] in ids:
            count += 1
            doc['id'] = candidate_id + '%s' % chr(96 + count) # 97 = ascii 'a'
        ids.add(doc['id'])
        doc['telescope'], doc['configuration'], doc['sub'], doc['nant'] =\
            doc['tele_conf_sub_nant'].split(':')
        yield doc

docs = _docs(open('data.csv'), quotechar=None)
